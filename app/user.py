# from app import app
# from flask import jsonify, request
# from app.firebase import *


# # @app.route("/user/create", methods=["GET"])
# def makeUser(userEmail, password):
#     userEmail = userEmail[:userEmail.find("@")]
#     password = request.args.get("password")
#     addUsertoDB(userEmail,password)
#     # return jsonify(message="Successfully added new user")

# def checkUser(userEmail):
#     userEmail = userEmail[:userEmail.find("@")]
#     ref = db.reference(f'{userEmail}')
#     snapshot = ref.get()
#     return snapshot is not None
#     return jsonify(result=(snapshot is not None))

# def getUserPW(userEmail):
#     userEmail = userEmail[:userEmail.find("@")]
#     ref = db.reference(f'{userEmail}')
#     return ref.get()

# def login(userEmail, password):
#     if not checkUser(userEmail):
#         return "Wrong Email!"
#     userPW = getUserPW(userEmail)['password']
#     if not password == userPW:
#         return "Wrong Password!"
#     return "You are logged in"
    