import os
import random
import re

from keras.models import load_model
from DatasetGeneratorAI.ScrapperComponent.src.ScrapperModule import ScrapperModule
from DatasetGeneratorAI.AIComponent.src.AIModule import AIModule

class SmartAITrainer:

    def __init__(self, train_folder, validation_folder, train_epochs, flickr_api_key, flickr_secret):
        self.train_folder = train_folder
        self.validation_folder = validation_folder

        self.current_model = None
        self.AIModule = AIModule(epochs=train_epochs)
        self.scrappers = {}

        self.flickr_api_key = flickr_api_key
        self.flickr_secret = flickr_secret

        random.seed(42)

    def train(self, labels, model_name, iterations = 5):

        for label in labels:
            self.scrappers[label.labelName] = ScrapperModule(label.labelName, label.quantity / iterations, self.flickr_api_key, self.flickr_secret)

        for i in range(iterations):
            partial_model_name = model_name + '_partial_' + str(i) + '.h5'

            for label_idx, label in enumerate(labels):
                desired_qty = int(label.quantity / iterations)

                # Download desired_qty images for this label
                self.scrappers[label.labelName].search_download_exact(desired_qty, label.automaticFolder)

                if i > 0:
                    while True:
                        # Use current model to delete irrelevant images
                        qty_deleted = self.delete_irrelevant(label, label_idx, 0.5 + 0.05 * i)

                        # Only stop when ALL downloaded images are relevant, according to the current trained model
                        if qty_deleted == 0:
                            break

                        # Call scrapper again to download missing images for label
                        self.scrappers[label.labelName].search_download_exact(qty_deleted, label.automaticFolder)
                        pass

                # Reserve some of the new downloaded images for model validation while training
                self.train_validation_split(label, desired_qty)

            # Train new model using all downloaded images to this moment
            self.AIModule.train(self.train_folder, self.validation_folder, [ label.labelName for label in labels ], partial_model_name)

            # If it's the last iteration, rename temp model to final model and exit
            if i == iterations - 1:
                os.rename(partial_model_name, model_name)
                return

            # Load newly trained model into memory
            self.current_model = load_model(partial_model_name)


    def train_validation_split(self, label, qty_new_images, validation_ratio = 0.25):

        files = os.listdir(label.automaticFolder)

        digits = re.compile(r'(\d+)')
        # Natural order sorting
        files.sort(key=lambda x: tuple(int(token) if match else token
                 for token, match in
                 ((fragment, digits.search(fragment))
                  for fragment in digits.split(x))))

        for file in files[-qty_new_images:]:
            src = os.path.join(label.automaticFolder, file)
            dst_dir = os.path.join(self.validation_folder, label.labelName)
            os.makedirs(dst_dir, exist_ok=True)

            dst = os.path.join(dst_dir, file)
            if random.random() < validation_ratio:
                os.rename(src, dst)


    def delete_irrelevant(self, label, label_pred_index, min_score = 0.55):
        predictions = self.AIModule.predict(label.automaticFolder, self.current_model)
        files = os.listdir(label.automaticFolder)
        deleted_count = 0

        for i, p in enumerate(predictions):
            if p[label_pred_index] < min_score:
                os.remove(os.path.join(label.automaticFolder, files[i]))
                deleted_count += 1

        return deleted_count