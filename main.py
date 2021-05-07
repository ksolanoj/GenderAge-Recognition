# Imports
import os
from flask import Flask, jsonify, request
from flask_cors import CORS
from FirebaseManager import (uploadImage, downloadImage)

# App creation
app = Flask(__name__)
CORS(app)


RESPONSE_TEMPLATE = {
    "response": None,
    "imageURL": ""
}

# Routes
@app.route('/', methods = ['GET'])
def test():
    return '<h1> Gender&Age Recognition API <h1/>'

@app.route('/detectFaces', methods = ['POST'])
def detectFaces():
    finalResponse = RESPONSE_TEMPLATE
    imageName = request.json['imageName']
    response = downloadImage(imageName)
    imageURL = uploadImage(imageName)
    finalResponse['response'] = response
    finalResponse['imageURL'] = imageURL
    if os.path.isfile("./detected/{0}.jpg".format(imageName)) and os.path.isfile("./downloaded/{0}.jpg".format(imageName)):
        os.remove("./detected/{0}.jpg".format(imageName))
        os.remove("./downloaded/{0}.jpg".format(imageName))
    return jsonify(finalResponse)


