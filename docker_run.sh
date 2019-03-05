docker run --restart always \
           -dti --privileged \
           --net=host --ipc=host -p 8666:8666 \
           -e DISPLAY=$DISPLAY \
           -v /tmp/.X11-unix:/tmp/.X11-unix \
           --name deepomatic_face_detection \
           deepomatic_face_detection