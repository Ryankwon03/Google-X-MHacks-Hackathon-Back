# Modules

from app import app
from flask import jsonify, request
from modules.ai import *
from app.gitReader import *
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

def getRepoInfo(repoName="p4-drones", AuthKey="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"):
    # AuthKey = request.args.get("AuthKey")
    # repoName = request.args.get("repoName")
    g = login(AuthKey)
    # g = login("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")
    curRepo = getRepo(g,repoName)
    contents = getAllContents(curRepo)
    processedList = makeList(curRepo,contents)
    return processedList

@app.route("/init", methods=["GET"])
def initProject():
    # repoName = request.args.get("repoName")
    # AuthKey = request.args.get("AuthKey")
    repoInfo = getRepoInfo()
    model = declare_model()
    chat = text_init(model)
    print(gemini_chat_send(chat,repoInfo))
    print("I am done!!!!!!!!!!!!!!!")
    return jsonify(message="hello,done")
