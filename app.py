# Imports
from flask import Flask, jsonify, request
from FirebaseManager import (uploadImage, downloadImage)


# App creation
app = Flask(__name__)


# Constants
PORT = 4000

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
    return jsonify(finalResponse)

if __name__ == '__main__':
    app.run(debug = True, port = PORT)

