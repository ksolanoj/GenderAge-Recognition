# Imports
import cv2
import math
import time 

# Functions
def getFaceBox(net, frame, conf_threshold = 0.7):
    frameOpencvDnn = frame.copy()
    frameHeight = frameOpencvDnn.shape[0]
    frameWidth = frameOpencvDnn.shape[1]
    blob = cv2.dnn.blobFromImage(frameOpencvDnn, 1.0, (300, 300), [104, 117, 123], True, False)
    net.setInput(blob)
    detections = net.forward()
    bboxes = []
    for i in range(detections.shape[2]):
        confidence = detections[0, 0, i, 2]
        if confidence > conf_threshold:
            x1 = int(detections[0, 0, i, 3] * frameWidth)
            y1 = int(detections[0, 0, i, 4] * frameHeight)
            x2 = int(detections[0, 0, i, 5] * frameWidth)
            y2 = int(detections[0, 0, i, 6] * frameHeight)
            bboxes.append([x1, y1, x2, y2])
            cv2.rectangle(frameOpencvDnn, (x1, y1), (x2, y2), (0, 255, 0), int(round(frameHeight / 150)), 8)
    return frameOpencvDnn, bboxes

# Code

MODEL_MEAN_VALUES = (78.4263377603, 87.7689143744, 114.895847746)

ageList = ['(0-2)', '(4-6)', '(8-12)', '(15-20)', '(25-32)', '(38-43)', '(48-53)', '(60-100)']

genderList = ['Male', 'Female']

faceProto = './models/opencv_face_detector.pbtxt'
faceModel = './models/opencv_face_detector_uint8.pb'

ageProto = './models/age_deploy.prototxt'
ageModel = './models/age_net.caffemodel'

genderProto = './models/gender_deploy.prototxt'
genderModel = './models/gender_net.caffemodel'

ageNet = cv2.dnn.readNetFromCaffe(ageProto, ageModel)
genderNet = cv2.dnn.readNetFromCaffe(genderProto, genderModel)
faceNet = cv2.dnn.readNet(faceModel, faceProto)

def detectImage(imagePath, imageName):
    response = []
    padding = 20
    frame = cv2.imread(imagePath)
    frameFace, bboxes = getFaceBox(faceNet, frame)
    if not bboxes:
        response.append({"Message":"No Faces Detected on the image."})
    for bbox in bboxes:        
        face = frame[max(0,bbox[1]-padding):min(bbox[3]+padding,frame.shape[0]-1),max(0,bbox[0]-padding):min(bbox[2]+padding, frame.shape[1]-1)]
        blob = cv2.dnn.blobFromImage(face, 1.0, (227, 227), MODEL_MEAN_VALUES, swapRB=False)

        genderNet.setInput(blob)
        genderPreds = genderNet.forward()
        gender = genderList[genderPreds[0].argmax()]
        genderCofidence = genderPreds[0].max()

        ageNet.setInput(blob)
        agePreds = ageNet.forward()
        age = ageList[agePreds[0].argmax()]
        ageConfidence = agePreds[0].max()

        response.append({"gender":gender, "genderCofidence":genderCofidence, "age": age, "ageCofidence":ageConfidence})
        cv2.imwrite('detected/{0}.jpg'.format(imageName), frameFace)
    return response
    











