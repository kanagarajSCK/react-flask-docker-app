import base64
import cv2
import numpy as np
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
model_path = os.path.join(BASE_DIR, 'models')

face_proto = os.path.join(model_path, "opencv_face_detector.pbtxt")
face_model = os.path.join(model_path, "opencv_face_detector_uint8.pb")
age_proto = os.path.join(model_path, "age_deploy.prototxt")
age_model = os.path.join(model_path, "age_net.caffemodel")
gender_proto = os.path.join(model_path, "gender_deploy.prototxt")
gender_model = os.path.join(model_path, "gender_net.caffemodel")

MODEL_MEAN_VALUES = (78.4263377603, 87.7689143744, 114.895847746)
age_buckets = ['(0-2)', '(5-6)', '(8-12)', '(20-25)', '(20-25)', '(38-43)', '(48-53)', '(60-100)']
gender_list = ['Male', 'Female']

face_net = cv2.dnn.readNet(face_model, face_proto)
age_net = cv2.dnn.readNet(age_model, age_proto)
gender_net = cv2.dnn.readNet(gender_model, gender_proto)

def highlight_face(net, frame, conf_threshold=0.7):
    h, w = frame.shape[:2]
    blob = cv2.dnn.blobFromImage(frame, 1.0, (300, 300), [104, 117, 123], True, False)
    net.setInput(blob)
    detections = net.forward()
    face_boxes = []

    for i in range(detections.shape[2]):
        confidence = detections[0, 0, i, 2]
        if confidence > conf_threshold:
            x1 = int(detections[0, 0, i, 3] * w)
            y1 = int(detections[0, 0, i, 4] * h)
            x2 = int(detections[0, 0, i, 5] * w)
            y2 = int(detections[0, 0, i, 6] * h)
            face_boxes.append([x1, y1, x2, y2])
    return face_boxes

def detect_age_gender(frame):
    face_boxes = highlight_face(face_net, frame)
    detections = []

    for (x1, y1, x2, y2) in face_boxes:
        face = frame[y1:y2, x1:x2]
        if face.shape[0] < 10 or face.shape[1] < 10:
            continue

        blob = cv2.dnn.blobFromImage(face, 1.0, (227, 227), MODEL_MEAN_VALUES, swapRB=False)

        gender_net.setInput(blob)
        gender = gender_list[gender_net.forward().argmax()]

        age_net.setInput(blob)
        age = age_buckets[age_net.forward().argmax()]

        label = f"{gender}, {age}"
        detections.append({'box': [x1, y1, x2, y2], 'label': label})

        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
        cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2, cv2.LINE_AA)

    _, buffer = cv2.imencode('.jpg', frame)
    encoded_img = base64.b64encode(buffer).decode('utf-8')

    return encoded_img, detections
