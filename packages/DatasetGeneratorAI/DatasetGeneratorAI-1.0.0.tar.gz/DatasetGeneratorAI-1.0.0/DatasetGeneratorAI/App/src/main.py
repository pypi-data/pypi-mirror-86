import sys

from requests import api
sys.path.append('../../')

import base64
import requests

import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

from App.src.label import Label
from App.src.smartAITrainer import SmartAITrainer

AITrainer = SmartAITrainer(train_folder='Data/automatic/train', validation_folder='Data/automatic/test', train_epochs=10, flickr_api_key='8e38b5c1b77f778d2a084f865e368520', flickr_secret='13671185dd560173')
model_name = 'trainer_model.h5'

api_url = 'http://localhost:49166/api'
test_image = 'cat.jpg'

def generate_model():
    labels = []
    labels.append(Label(labelName='cat', automaticFolder='Data/automatic/train/cat', quantity=5000))
    labels.append(Label(labelName='dog', automaticFolder='Data/automatic/train/dog', quantity=5000))
    
    AITrainer.train(labels, model_name, iterations=4)

def upload_model():
    model_data = open(model_name, 'rb').read()
    model_b64 = base64.b64encode(model_data).decode('ascii')

    post_data = {
        'ClassName': 'cat',
        'ModelBase64': model_b64
    }

    api_response = requests.post(api_url + '/ClassModel', json=post_data)

    if api_response.status_code == 201:
        print("Model uploaded")

def test_model_api():
    img_data = open(test_image, 'rb').read()
    img_b64 = base64.b64encode(img_data).decode('ascii')

    post_data = {
        'ImageBase64': img_b64,
        'Classes': [ 'cat' ]
    }

    api_response = requests.post(api_url + '/Classification', json=post_data)
    print(api_response.json())


#generate_model()
upload_model()
test_model_api()