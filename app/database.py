# import firebase_admin
# from firebase_admin import credentials, db

# cred = credentials.Certificate("credentials.json")
# firebase_admin.initialize_app(cred, {"databaseURL" : "https://hackathon-new-f76fe-default-rtdb.firebaseio.com/"})

# def getDBSize():
#     return db.reference("/curSize").get()

# def addSize():
#     cursize = getDBSize()
#     db.reference("/curSize").set(cursize + 1)

# def addUsertoDB(userEmail,password):
#     size = getDBSize()
#     newRef = db.reference("/ssssss")
#     user_data = {
#         "password" : password
#     }
#     newRef.set(user_data)
#     addSize()

# # ref = db.reference("/")

# # userRef = db.reference("/User2")
# # user_data = {
# #     'FirstName' : "Sungmo",
# #     'LastName': "Kwon"
# # }
# # userRef.set(user_data)
# # print(ref.get())