# Modules

from app import app
from flask import jsonify, request
from modules.ai import *
from app.gitReader import *
from app.user import *
from app.helper import *
from app.firebase import *
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

@app.route("/init", methods = ["POST"])
def initProject():
    data=request.get_json()
    repoName = data["repoName"]
    AuthKey = data["authKey"]
    repoInfo = getRepoInfo(repoName,AuthKey)
    model = declare_model()
    chat = text_init(model)
    geminiResponse=gemini_chat_send(chat,repoInfo)
    save_to_firebase("ianpark0412","p4-drones", json.dumps(str(geminiResponse[0])))
    save_chat_to_txt(json.dumps(str(geminiResponse[0])), "ianpark_p4-drones")

    return jsonify(message=f"succesfully read the repo {repoName}.", geminiResponse=geminiResponse[1])

@app.route("/user/signup", methods=["POST"])
def newUserSignup():
    data = request.get_json()
    try:
        user = auth.create_user(
            email=data['email'],
            password=data['password']
        )
        return jsonify(statusCode=200, message=f"Successfully created user: {user.uid} ({user.email}) ")
    except Exception as error:
        return jsonify(statusCode=400, message=f'{str(error)}')

    # data = request.get_json()
    # userEmail = data['userEmail']
    # userID = userEmail[:userEmail.find("@")]
    # if checkUser(userID):
    #     return jsonify(statuscode=409, message="User already exists")
    # return jsonify(statuscode=200, message=f'User {userEmail} successfully signed up!')


# @app.route("/user/login", methods=["POST"])
# def userLogin():
#     data = request.get_json()
#     try:
#         usercred = auth.get_user_by_email()
#         user = auth.sign_in_with_email_and_password(data['email'], data['password'])
#         return jsonify(statusCode=200, message=f"Successfully signed in user: {user.uid} ({user.email})")
#     except Exception as error:
#         return jsonify(statusCode=400, message=f'{str(error)}')

# curl -d "@data.json" -H "Content-Type: application/json" -X POST http://localhost:3000/signup
