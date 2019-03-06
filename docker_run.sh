docker run --restart always \
           -dti --privileged \
           -p 8666:8666 \
           --name deepomatic_face_detection \
           deepomatic_face_detection

# -e DISPLAY=$DISPLAY \
# -v /home/pierre/deepomatic_data/face_recognition/examples:/root/face_recognition/examples \
