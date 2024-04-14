import firebase_admin
from firebase_admin import credentials, db, firestore, auth

cred = credentials.Certificate("credentials.json")
firebase_admin.initialize_app(cred, {"databaseURL" : "https://hackathon-new-f76fe-default-rtdb.firebaseio.com/"})

firestore_db = firestore.client()

def get_chromadb_size():
    ref = db.reference("/curChromadbSize")
    return ref.get()

def increase_chromadb_size_1():
    ref = db.reference("/curChromadbSize")
    curVal = ref.get()
    ref.set(curVal + 1)

def getProjectNamewithProjectid(userid,projectid):
    projectRef = firestore_db.collection(userid).document(projectid)
    projectDoc = projectRef.get()
    return projectDoc.to_dict()['projectName']

def getProjectData(userid,projectid):
    projectRef = firestore_db.collection(userid).document(projectid)
    projectDoc = projectRef.get().to_dict()
    return projectDoc


def getChatHistoryfromFireStore(userid,projectid):
    doc_ref = firestore_db.collection(userid).document(projectid)
    doc = doc_ref.get()
    curChatList = doc.to_dict()['user_chat_history']
    return curChatList


def appendChatHistorytoFireStore(userid, projectid, chatList):
    doc_ref = firestore_db.collection(userid).document(projectid)
    doc = doc_ref.get()
    curChatList = doc.to_dict()['user_chat_history']
    curChatList.append(chatList)
    print(curChatList)

    doc_ref.update({
        'user_chat_history' : curChatList
    })


def saveProjecttoFireStore(userid, projectName, train_history,techTags):
    data = {
        'projectName' : projectName,
        'train_history' : train_history,
        'user_chat_history' : [],
        'techTags' : techTags
    }
    document_ref = firestore_db.collection(userid).document()
    document_ref.set(data)
    return document_ref.id

def deleteFromFireStore(userid,projectid):
    doc_ref = firestore_db.collection(userid).document(projectid)
    doc_ref.delete()