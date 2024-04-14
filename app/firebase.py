import firebase_admin
from firebase_admin import credentials, db, firestore, auth

cred = credentials.Certificate("credentials.json")
firebase_admin.initialize_app(cred, {"databaseURL" : "https://hackathon-new-f76fe-default-rtdb.firebaseio.com/"})

firestore_db = firestore.client()

def getProjectNamewithProjectid(userid,projectid):
    projectRef = firestore_db.collection(userid).document(projectid)
    projectDoc = projectRef.get()
    print(projectDoc)
    return projectDoc.to_dict()['projectName']


def saveProjecttoFireStore(userid, projectName, train_history):
    data = {
        'projectName' : projectName,
        'train_history' : train_history
    }
    document_ref = firestore_db.collection(userid).document()
    document_ref.set(data)
    return document_ref.id

