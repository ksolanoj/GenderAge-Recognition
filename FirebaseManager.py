import pyrebase
import time
from FaceRecognitionManager import *

firebaseConfig = {
    "apiKey": "AIzaSyCPera806NQnThRLv10pURrWa9GkrUKqYs",
    "authDomain": "iaproject-29018.firebaseapp.com",
    "projectId": "iaproject-29018",
    "storageBucket": "iaproject-29018.appspot.com",
    "messagingSenderId": "817053540910",
    "appId": "1:817053540910:web:423251c3f6691e27fd75bf",
    "databaseURL" : ""
}

firebase = pyrebase.initialize_app(firebaseConfig)
storage = firebase.storage()

def uploadImage(imageName):
    globalPath = "detected/{0}.jpg".format(imageName)
    storage.child(globalPath).put(globalPath)
    return

def downloadImage(imageName):
    globalPath = "uploaded/{0}.jpg".format(imageName)
    downloadPath = 'downloaded/{0}.jpg'.format(imageName)
    storage.child(globalPath).download(downloadPath)
    return detectImage(downloadPath, imageName)

print(downloadImage('image3'))

















