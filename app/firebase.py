import firebase_admin
from firebase_admin import credentials, db, firestore, auth

cred = credentials.Certificate("credentials.json")
firebase_admin.initialize_app(cred, {"databaseURL" : "https://hackathon-new-f76fe-default-rtdb.firebaseio.com/"})

firestore_db = firestore.client()

def save_to_firebase(userEmail, repoName, chat_history):
    data = {
        'chat_history' : chat_history
    }
    document_ref = firestore_db.collection('projectFiles').document()
    document_ref.set(data)
    print('Document ID:', document_ref.id)


def getDBSize():
    return db.reference("/curSize").get()

def addSize():
    cursize = getDBSize()
    db.reference("/curSize").set(cursize + 1)

def addUsertoDB(userID,password):
    size = getDBSize()
    user_data = {
        "password" : password
    }
    db.reference(f'/users/{userID}').set(user_data)
    # db.reference(f'/users/{userID}/password').set(password)
    addSize()