import requests

url='http://localhost:8080/recognize_face'
files={'image': open('deepomatic_faces/test/19983214_243521042832746_7866257885413814144_o.jpg','rb')}
r = requests.post(url,files=files)
print(r.json())