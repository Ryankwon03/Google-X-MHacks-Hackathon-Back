# Modules

from app import app
from flask import jsonify, request
from modules.ai import *
from app.gitReader import *
from app.user import *
from app.helper import *
from app.firebase import *
from app import FIREBASE_API_KEY
import requests
import json


@app.route("/")
def index():
    return jsonify(message="hello!")

def getRepoInfo(repoName,AuthKey):
    g = logintoGithub(AuthKey)
    curRepo = getRepo(g,repoName)
    contents = getAllContents(curRepo)
    processedList = makeListFromRepo(curRepo,contents)
    return processedList

def addProjecttoUserID(userid,projectid):
    userRef = db.reference(f'/users/{userid}/projectList')
    # USER HAS NO PROJECTS
    if userRef.get() == None:
        projectList = [projectid]
        userRef.set(projectList)
    
    # USER HAS PROJECTS
    else:
        curList = userRef.get()
        curList.append(projectid)
        userRef.set(curList)
    return userRef.get()


    

@app.route("/project/init", methods = ["POST"])
def initProject():
    data=request.get_json()
    repoName = data["repoName"]
    authKey = data["authKey"]
    userid = data["userid"]
    projectName = data["projectName"]
    repoInfo = getRepoInfo(repoName,authKey)
    model = declare_model()
    chat = text_init(model)
    geminiResponse=gemini_chat_send(chat,repoInfo)
    print(geminiResponse)
    print(geminiResponse[0])
    train_history = json.dumps(str(geminiResponse[0]))
    print(train_history)

    projectid = saveProjecttoFireStore(userid,projectName, json.dumps(str(geminiResponse[0])))
    print(projectid)
    addProjecttoUserID(userid,projectid)

    return jsonify(message=f"succesfully read the repo {repoName}.", geminiResponse=geminiResponse[1])

def addUsertoRealTimeDB(userid, data):
    userRef = db.reference(f'/users/{userid}')
    user_data = {
        "email" : data['email'],
        "firstName" : data['firstName'],
        "lastName" : data['lastName']
    }
    userRef.set(user_data)

@app.route("/user/signup", methods=["POST"])
def newUserSignup():
    data = request.get_json()
    try:
        user = auth.create_user(
            email=data['email'],
            password=data['password']
        )
        # link = auth.generate_password_reset_link(data['email'],action_code_settings=None)
        addUsertoRealTimeDB(user.uid,data)
        return jsonify(statusCode=200, message=f"Successfully created user: {user.uid} ({user.email})", userid=user.uid)
    except Exception as error:
        return jsonify(statusCode=400, message=f'{str(error)}')

    # data = request.get_json()
    # userEmail = data['userEmail']
    # userID = userEmail[:userEmail.find("@")]
    # if checkUser(userID):
    #     return jsonify(statuscode=409, message="User already exists")
    # return jsonify(statuscode=200, message=f'User {userEmail} successfully signed up!')


def getUserIDfromLogin(email):
    user = auth.get_user_by_email(email)
    return user.uid

@app.route("/user/login", methods=["POST"])
def userLogin():
    data = request.get_json()
    request_ref = "https://www.googleapis.com/identitytoolkit/v3/relyingparty/verifyPassword?key={0}".format(FIREBASE_API_KEY)
    myHeader = {"content-type": "application/json"}
    data = json.dumps({"email":data['email'], "password": data['password'], "returnSecureToken": True})
    request_object = requests.post(request_ref, headers=myHeader, data=data).json()
    if "email" in request_object:
        print("successful login!")
        userid = getUserIDfromLogin(request_object['email'])
        return jsonify(statusCode=200, message="Login Successful", userID=userid)
    else:
        return jsonify(statusCode=400, message=request_object['error'])
    # try:
    #     request_ref = "https://www.googleapis.com/identitytoolkit/v3/relyingparty/verifyPassword?key={0}".format("d2df986c2b5d8dbe628b22276e93c240527770b4")
    #     myHeader = {"content-type": "application/json"}
    #     data = json.dumps({"email":data['email'], "password": data['password'], "returnSecureToken": True})
    #     request_object = requests.post(request_ref, headers=myHeader, data=data)
    #     return request_object.json()
    #     user = auth.sign_in_with_email_and_password(data['email'], data['password'])
    #     return jsonify(statusCode=200, message=f"Successfully signed in user: {user.uid} ({user.email})")
    # except Exception as error:
    #     return jsonify(statusCode=400, message=f'{str(error)}')

# curl -d "@data.json" -H "Content-Type: application/json" -X POST http://localhost:3000/signup
