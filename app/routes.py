# Modules

from app import app
from flask import jsonify, request
from modules.ai import *
from app.gitReader import *
from app.user import *
from app.helper import *
import json


@app.route("/")
def index():
    return jsonify(message="hello!")


@app.route("/makeProject", methods=["POST"])
def makeProject():
    data = request.get_json()
    Authkey = data["AuthKey"]
    repoName = data["repoName"]

def getRepoInfo(repoName,AuthKey):
    # AuthKey = request.args.get("AuthKey")
    # repoName = request.args.get("repoName")
    g = login(AuthKey)
    # g = login("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")
    curRepo = getRepo(g,repoName)
    contents = getAllContents(curRepo)
    processedList = makeList(curRepo,contents)
    return processedList

@app.route("/init")
def initProject():
    data=request.get_json()
    repoName = request.args.get("repoName")
    AuthKey = request.args.get("AuthKey")
    # repoInfo = getRepoInfo("p4-drones", "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")
    repoInfo = getRepoInfo(repoName,AuthKey)
    model = declare_model()
    chat = text_init(model)
    geminiResponse=gemini_chat_send(chat,repoInfo)
    return jsonify(message=f"succesfully read the repo {repoName}.", geminiResponse=geminiResponse)

# @app.route("/signup", methods=["POST"])
# def newUserSignup():
#     data = request.get_json()
#     userEmail = data['userEmail']
#     password = data['password']
#     if not checkUser(userEmail):
#         makeUser(userEmail, password)
#         return jsonify(message=f'User {userEmail} successfully signed up!', res=checkUser("jiohin"))
#     return jsonify(message="User already exists with email")


# @app.route("/login")
# def userLogin():
#     res = login("ianpark0412@gmail.com", "1234")
#     return jsonify(res = res)

# curl -d "@data.json" -H "Content-Type: application/json" -X POST http://localhost:3000/signup
