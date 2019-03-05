import face_recognition
import cv2
import os
from face_recognition_knn import predict
import pickle

# This is a super simple (but slow) example of running face recognition on live video from your webcam.
# There's a second example that's a little more complicated but runs faster.

# PLEASE NOTE: This example requires OpenCV (the `cv2` library) to be installed only to read from your webcam.
# OpenCV is *not* required to use the face_recognition library. It's only required if you want to run this
# specific demo. If you have trouble installing it, try any of the other demos that don't require it instead.

# Get a reference to webcam #0 (the default one)
video_capture = cv2.VideoCapture(0)

# known_face_encodings = []

# for image in ["zoe.jpg", "vincent.png", "viem.png", "thomas_r.png", "thomas_t.png", "thibaut.jpg", "si.jpg", "sabrina.png", "romane.jpg", "quentin.png", "pierre.jpg", "nicolas.png", "marion.png", "marine.png", "lingyao.png", "leo.png", "kemy.png", "jesse.jpg", "hugo.jpg", "eleonore.jpg", "cecile.jpg", "augustin.png", "antje.jpg", "alois.png", "alexis.png", "alexandre.jpg"]:

#     # Load a second sample picture and learn how to recognize it.
#     face = face_recognition.load_image_file(os.path.join("deepomatic_faces", image))
#     face_encoding = face_recognition.face_encodings(face)[0]

#     known_face_encodings.append(face_encoding)

# known_face_names = ["zoe", "vincent", "viem", "thomas_r", "thomas_t", "thibaut", "si", "sabrina", "romane", "quentin", "pierre", "nicolas", "marion", "marine", "lingyao", "leo", "kemy", "jesse", "hugo", "eleonore", "cecile", "augustin", "antje", "alois", "alexis", "alexandre"]

model_path = "deepomatic_faces_trained_knn_model.clf"
with open(model_path, 'rb') as f:
    knn_clf = pickle.load(f)

while True:
    # Grab a single frame of video
    ret, frame = video_capture.read()

    # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
    rgb_frame = frame[:, :, ::-1]

    # Find all the faces and face enqcodings in the frame of video
    # face_locations = face_recognition.face_locations(rgb_frame)
    # face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

    predictions = predict(rgb_frame, model=knn_clf)

    print(predictions)

    if len(predictions) == 0:
        print("No face")

    # Loop through each face in this frame of video
    for name, (top, right, bottom, left) in predictions: #zip(face_locations, face_encodings):
        # See if the face is a match for the known face(s)
        # matches = face_recognition.compare_faces(known_face_encodings, face_encoding)

        # name = "Unknown"

        # If a match was found in known_face_encodings, just use the first one.
        # if True in matches:
        #     first_match_index = matches.index(True)
        #     name = known_face_names[first_match_index]

        print(name)

        # Draw a box around the face
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

        # Draw a label with a name below the face
        cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

    # Display the resulting image
    # cv2.imshow('Video', frame)

    # Hit 'q' on the keyboard to quit!
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release handle to the webcam
video_capture.release()
cv2.destroyAllWindows()
