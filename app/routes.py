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


@app.route("/test")
def test(): 
    history = gemini_chat()
    ret = []
    for thing in history:
        this = (str(thing.parts))
        print(this)
        ret.append(this)
    
    print(ret)
    return jsonify(message="yes", result=ret)

@app.route("/getRepo")
def les():
    # AuthKey = request.args.get("AuthKey")
    repoName = request.args.get("repoName")
    g = login("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")
    # g = login("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")
    curRepo = getRepo(g,repoName)
    contents = getAllContents(curRepo)
    return makeList(curRepo,contents)


