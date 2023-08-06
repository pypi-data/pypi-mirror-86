import os

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

from AIComponent.src.AIModule import AIModule
from argparse import ArgumentParser

from keras.models import load_model

parser = ArgumentParser()
parser.add_argument("-m", "--model", dest="model_file_path", help="Keras model file path", required=True)
parser.add_argument("-i", "--image", dest="image_file_path", help="Image path to predict", required=True)

args = parser.parse_args()

model = load_model(args.model_file_path)
ai_module = AIModule()

prediction = ai_module.predict_single(args.image_file_path, model)

print(prediction[0])