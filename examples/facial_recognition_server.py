from bottle import run, post, request
import face_recognition

@post('/recognize_face')
def recognize_face():
   img = request.files['image']
   print(img.file)


run(host='localhost', port=8080)