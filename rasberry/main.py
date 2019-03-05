# -*- coding: utf-8 -*-

import cv2
import threading
import requests
from PIL import Image
from io import BytesIO
import os
import time
import logging
import random

logging.basicConfig(level='INFO',
                    format='[%(levelname)s %(name)s %(asctime)s %(process)d %(thread)d %(filename)s:%(lineno)s] %(message)s')

LOCK = threading.Lock()
FRAMES = []

IMAGE_FILE = '/tmp/cam.jpg'
URL = 'http://dahlia:8666/recognize_face'

SENTENCES = {
    "lingyao" : ["Lynegyao", "Lynegyao, merci pour ses douces friandises chinoises"],
    "thomas_t" : ["Thomas", "Thomas, j'ai hâte que vous notiez le café aujourd'hui"],
    "thomas_r": ["Thomas", "Thomas, s'il vous plaît, ne me dénoncez pas à la CNIL"],
    "eleonore" : ["Lilo", "éléonore tezenas dumoncelle, quand nous invitez vous dans votre chateau ?"],
    "antje": ["Antieux"],
    "kemy": ["Kémy", "Lekème, je suis un grand fan de votre travail et de votre trotinette"],
    "leo": ["Léo", "Léo, le conseil d'administration de Péèssa vous attend en salle colisée"],
    "viem": ["Viem", "protectrice de la nature"],
    "cecile":  ["Cécile", "Cécile, ca close ou ca close pas aujourd'hui ?"],
    "marine": ["marine", "Insta Yoga gueurl, n'oublies pas de faire ton tchèque ine ce matin"],
    "alois": ["Alohiss", "Alohiss, prêt à dynhguer aujourd'hui ?"],
    "augustin": ["Augustin", "Guce", "Patron"],
    'unknown': ['Bel inconnu'],
    "alexis": ["Alexis", "vieille fripouille"],
    "vincent": ["Vinssant", "Vichèneté, jusqu'à quelle heure as tu codé hier ?"],
    "hugo" : ["Hugo", "mon créateur"],
    "pierre": ["Pierre", "mon Père fondateur"],
    "zoe": ["Zoé", "Zorrette, j'espère que tu n'as pas commandé de nouvelle chaussure aujourd'hui"],
    "romane": ["Romane", "Romane, alors on le fait ce séminère à Baly ?"],
    "alexandre": ["Alexandre", "Alexandre, je te met une branlée au baby quand tu veux"],
    "quentin": ["Quentin", "Quentin, mise en prod de tôte a 14 heure"],
    "thibaut" : ["Thibaut", "Thibaut, vesta de la segmentation prévu pour demain soir"],
    "sabrina": ["sabrina", "Sabinouche, le front end, c'est ma passion à moi aussi"],
    "marion": ["Marion", "Marionnette, si vous avez des questions sur Bellerone, je suis expert en apprentissage profond, je suis moi même un réseau de neurone"],
    "nicolas": ["Nicolas", "Nicolas, je suis très fière de voir que tu apprends à coder, les commerciaux devraient prendre exemple sur toi"],
}

def most_common(lst):
    return max(set(lst), key=lst.count)

def post():
    global FRAMES
    history = []
    previous_name = None
    history_len = 3
    while True:
        try:
            with LOCK:
                # we always take the last frame to avoid lagging behind
                if not FRAMES:
                    time.sleep(0.001)
                    continue
                frame = FRAMES.pop()
                FRAMES = []
                
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            cv2.imwrite(IMAGE_FILE, rgb_frame)

            with open(IMAGE_FILE, 'rb') as img:
                r = requests.post(URL, files={'image': img})
            # unknown can appear twice in the same frame
            results = list(set([res['name'] for res in r.json()['results']]))
            logging.info("RESULTS={}".format(results))
            if not results:
                history = []
                previous_name = None
                continue
            
            history.append(results)
            history = history[-history_len:]

            if len(history) < history_len:
                continue

            logging.info("HISTORY={}".format(history))
            flatten = []
            for img_pred in history:
                 flatten += img_pred
                 
            logging.info("FLATTEN={}".format(flatten))
            name = most_common(flatten)
            if name != previous_name:
                say_hello(name)
            previous_name = name
        except IOError:
            pass

def recognize():
    cam = cv2.VideoCapture(0)
    i = 0
    history = []
    while True:
        ret, frame = cam.read()
        # in this thread we must keep reading the cam to avoid lag
        with LOCK:
            FRAMES.append(frame)
        
def say_hello(name):
    if name in SENTENCES:
        lst = SENTENCES[name]
        idx = random.randint(0, len(lst) - 1)
        suffix = lst[idx]
    else:
        suffix = name.capitalize()
    os.system('pico2wave -l fr-FR -w bonjour.wav "Bonjour {}" && aplay bonjour.wav'.format(suffix))
        
if __name__ == '__main__':
    th = threading.Thread(target=post)
    th.start()
    recognize()

