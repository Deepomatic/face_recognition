from PIL import Image, ExifTags
import os

SIZE = (600, 600)
def resize_image(input_path, output_path):
    img = Image.open(input_path)
    if "JPG" == input_path[-3:]:
        exif=dict((ExifTags.TAGS[k], v) for k, v in img._getexif().items() if k in ExifTags.TAGS)
        img=img.rotate(270, expand=True)
    img.thumbnail(SIZE)
    img.save(output_path)

input_directory = "/home/pierre/deepomatic_data/face_recognition/examples/deepomatic_faces/train_save"
output_directory = "/home/pierre/deepomatic_data/face_recognition/examples/deepomatic_faces/train_2"

for d in os.listdir(input_directory):
    current_input_directory = os.path.join(input_directory, d)
    current_output_directory = os.path.join(output_directory, d)
    
    if not os.path.exists(current_output_directory):
        os.makedirs(current_output_directory)

    for i in os.listdir(current_input_directory):
        print(i)
        current_input_image = os.path.join(current_input_directory, i)
        current_output_image = os.path.join(current_output_directory, i)
        resize_image(current_input_image, current_output_image)