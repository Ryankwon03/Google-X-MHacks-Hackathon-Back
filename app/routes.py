# Modules

from app import app
from app import myChromaDB
from flask import jsonify, request
from modules.ai import *
from app.gitReader import *
from app.helper import *
from app.firebase import *
from app import FIREBASE_API_KEY
import requests
import json
from uuid import uuid4

def getBestQuery(text):
    results = myChromaDB.query(
        query_texts=[text],
        n_results=3,
        include=['distances','embeddings','documents']
    )
    return results['distances'][0], results['documents'][0], results['embeddings'][0]


@app.route("/debug/query/<input_text>")
def getQueryfromLocal(input_text):
    print(input_text)
    curQuery = getBestQuery(input_text)
    return jsonify(best_match_distance = curQuery[0], best_match_content = curQuery[1])

@app.route("/")
def index():
    results = myChromaDB.query(
        query_texts=["DFS algorithm and Map.cpp"],
        n_results=1
    )
    return jsonify(message="hello!", curSize = get_chromadb_size(), chromaResults = results)

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

def readProjectList(userid):
    userProjectListRef = db.reference(f'/users/{userid}/projectList')
    userProjectList = []
    for projectid in userProjectListRef.get():
        # print(projectid)
        projectName = getProjectNamewithProjectid(userid,projectid)
        entry = {'projectid' : projectid, 'projectName' : projectName}
        userProjectList.append(entry)
    return userProjectList



@app.route("/project/getChatHistory/<userid>/<projectid>", methods = ["GET"])
def getChatHistoryofProject(userid,projectid):
    userid = request.view_args['userid']
    projectid = request.view_args['projectid']
    chatList = getChatHistoryfromFireStore(userid,projectid)
    return jsonify(user_chat_history=chatList)



@app.route("/project/askQuestion", methods=["POST"])
def askQuestioninProject():
    data = request.get_json()
    projectData = getProjectData(data['userid'],data['projectid'])
    techTags = projectData['techTags']
    model = declare_model('1.5',techTags)
    chat = text_init(model)
    curBestQuery = getBestQuery(data['query'])
    # This is chat history
    geminiResponse=gemini_continue_asking(chat, projectData['train_history'], projectData['user_chat_history'],data['query'],curBestQuery[1])
    geminiAnswer = str(geminiResponse[5])[17:-17]
    curChat = {'user' : data['query'], 'model' : geminiAnswer}
    appendChatHistorytoFireStore(data['userid'],data['projectid'],curChat)

    return jsonify(geminiAnswer = geminiAnswer)

def deleteFromUser(userid, deleteProjectid):
    userProjectListRef = db.reference(f'/users/{userid}/projectList')
    userProjectList = []
    for projectid in userProjectListRef.get():
        if not projectid == deleteProjectid:
            userProjectList.append(projectid)
    userProjectListRef.set(userProjectList)


@app.route("/project/deleteProject", methods = ["DELETE"])
def deleteProject():
    data = request.get_json()
    deleteFromFireStore(data['userid'],data['projectid'])
    deleteFromUser(data['userid'],data['projectid'])
    return jsonify(statusCode=200, message="delte!!")


@app.route("/project/loadProjects/<userid>", methods=["GET"])
def loadProjectsasList(userid):
    # userid=request.args.get('userid')
    # print(userid)
    projectList = readProjectList(userid)
    return jsonify(projectList=projectList)


@app.route("/project/init", methods = ["POST"])
def initProject():
    data=request.get_json()
    # Reads the form data
    repoName = data["repoName"]
    authKey = data["authKey"]
    userid = data["userid"]
    projectName = data["projectName"]

    techTags = data["techTags"]

    # Reads Repo as List of Tuples
    repoInfo = getRepoInfo(repoName,authKey)

    # Gemini Training
    model = declare_model("1.5",techTags)
    chat = text_init(model)
    geminiResponse=gemini_chat_send(chat,repoInfo)

    # Add the Overview to Chromadb
    myChromaDB.add(
        documents=[geminiResponse[1]],
        ids=[str(get_chromadb_size())]
    )
    increase_chromadb_size_1()
    print("added Embedding to Chromadb")

    # Saving Informations to Database
    projectid = saveProjecttoFireStore(userid,projectName, json.dumps(str(geminiResponse[0])), techTags)
    # print(projectid)
    addProjecttoUserID(userid,projectid)

    return jsonify(message=f"succesfully read the repo {repoName}.", geminiResponse=geminiResponse[1], projectid=projectid)

# def addUsertoRealTimeDB(userid, data):
#     userRef = db.reference(f'/users/{userid}')
#     user_data = {
#         "email" : data['email'],
#         "firstName" : data['firstName'],
#         "lastName" : data['lastName']
#     }
#     userRef.set(user_data)


def checkUserExist(userid):
    ref = db.reference(f'/users/{userid}')
    snapshot = ref.get()
    return snapshot is not None


@app.route("/user/signin", methods=["POST"])
def userSignintoApp():
    data = request.get_json()
    userEmail = data['email']
    userid = userEmail[:userEmail.find("@")]
    userProjectRef = db.reference(f'/users/{userid}/projectList')
    # USER HAS NO PROJECTS
    # User Exists
    if checkUserExist(userid):
        return jsonify(isNew=False, userid=userid, hasProjects=(not userProjectRef.get() == None))
    else:
        newUserRef = db.reference(f'/users/{userid}')
        user_data = {
            "email" : data['email'],
            "firstName" : data['firstName'],
            "lastName" : data['lastName']
        }
        newUserRef.set(user_data)
        return jsonify(isNew=True,userid=userid, hasProjects=(userProjectRef.get() == None))
        


# @app.route("/user/signup", methods=["POST"])
# def newUserSignup():
#     data = request.get_json()
#     try:
#         user = auth.create_user(
#             email=data['email'],
#             password=data['password']
#         )
#         # link = auth.generate_password_reset_link(data['email'],action_code_settings=None)
#         addUsertoRealTimeDB(user.uid,data)
#         return jsonify(statusCode=200, message=f"Successfully created user: {user.uid} ({user.email})", userid=user.uid)
#     except Exception as error:
#         return jsonify(statusCode=400, message=f'{str(error)}')

#     # data = request.get_json()
#     # userEmail = data['userEmail']
#     # userID = userEmail[:userEmail.find("@")]
#     # if checkUser(userID):
#     #     return jsonify(statuscode=409, message="User already exists")
#     # return jsonify(statuscode=200, message=f'User {userEmail} successfully signed up!')


# def getUserIDfromLogin(email):
#     user = auth.get_user_by_email(email)
#     return user.uid

# @app.route("/user/login", methods=["POST"])
# def userLogin():
#     data = request.get_json()
#     request_ref = "https://www.googleapis.com/identitytoolkit/v3/relyingparty/verifyPassword?key={0}".format(FIREBASE_API_KEY)
#     myHeader = {"content-type": "application/json"}
#     data = json.dumps({"email":data['email'], "password": data['password'], "returnSecureToken": True})
#     request_object = requests.post(request_ref, headers=myHeader, data=data).json()
#     if "email" in request_object:
#         print("successful login!")
#         userid = getUserIDfromLogin(request_object['email'])
#         return jsonify(statusCode=200, message="Login Successful", userID=userid)
#     else:
#         return jsonify(statusCode=400, message=request_object['error'])
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
