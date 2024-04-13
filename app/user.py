from app import app
from flask import jsonify, request
from app.database import *

@app.route("/user/create", methods=["GET"])
def makeUser():
    # data = request.get_json()
    # userEmail = data["userEmail"]
    # password = data["password"]
    userEmail = request.args.get("userEmail")
    userEmail = userEmail[:userEmail.find("@")]
    password = request.args.get("password")
    addUsertoDB(userEmail,password)
    return jsonify(message="Successfully added new user")