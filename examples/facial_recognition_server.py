from bottle import run, get, post, request
import face_recognition
import cv2
import os
from face_recognition_knn import predict
import pickle
from PIL import Image
import io

model_path = "deepomatic_faces_trained_knn_model.clf"
with open(model_path, 'rb') as f:
    knn_clf = pickle.load(f)

@post('/recognize_face')
def recognize_face():
    img = request.files['image']

    img = face_recognition.load_image_file(img.file)

    predictions = predict(img, model=knn_clf)

    ret = []
    for name, (top, right, bottom, left) in predictions:
        current_box = {'top': top, 'right': right, 'bottom': bottom, 'left': left}
        ret.append({'name': name, 'box': current_box})

    return dict(data=ret)

run(host='localhost', port=8666)