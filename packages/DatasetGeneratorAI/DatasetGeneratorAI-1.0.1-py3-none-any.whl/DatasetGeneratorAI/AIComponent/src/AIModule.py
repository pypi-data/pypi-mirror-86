import os
from matplotlib.pyplot import cla
import numpy as np
import DatasetGeneratorAI.AIComponent.src.model as AIModel
import keras
from keras.preprocessing import image
from keras.optimizers import SGD
from matplotlib import pyplot as plt

class AIModule:
    def __init__(self, batch_size=32, epochs=5):
        self.batch_size = batch_size
        self.epochs = epochs
        self.IMG_HEIGHT = 192
        self.IMG_WIDTH = 192

    def train(self, train_folder, validation_folder, classes, model_name):

        # Model
        self.model = AIModel.get_model(len(classes))
        self.model.compile(optimizer=SGD(lr=0.001, momentum=0.9),
                           loss='categorical_crossentropy', metrics=['accuracy'])

        # dimensions of our images.
        img_width, img_height = self.IMG_HEIGHT, self.IMG_WIDTH

        epochs = self.epochs
        batch_size = self.batch_size

        # this is the augmentation configuration we will use for training
        train_datagen = image.ImageDataGenerator(
            rescale=1.0 / 255,
            shear_range=0.2,
            zoom_range=0.2,
            width_shift_range=0.1,
            height_shift_range=0.1,
            horizontal_flip=True)

        train_generator = train_datagen.flow_from_directory(
            train_folder,
            target_size=(img_width, img_height),
            batch_size=batch_size,
            class_mode='categorical',
            classes=classes,
            shuffle=True,
            seed=42)

        validation_datagen = image.ImageDataGenerator(rescale=1.0 / 255)

        validation_generator = validation_datagen.flow_from_directory(
            validation_folder,
            target_size=(img_width, img_height),
            batch_size=batch_size,
            class_mode='categorical',
            classes=classes,
            shuffle=True,
            seed=42)

        hist = self.model.fit(
            train_generator,
            steps_per_epoch=len(train_generator),
            epochs=epochs,
            validation_data=validation_generator,
            validation_steps=len(validation_generator),
            verbose=1)

        self.model.save(model_name)

        # plot loss
        plt.subplot(211)
        plt.title('Cross Entropy Loss')
        plt.plot(hist.history['loss'], color='blue', label='train')
        plt.plot(hist.history['val_loss'], color='orange', label='test')
        # plot accuracy
        plt.subplot(212)
        plt.title('Classification Accuracy')
        plt.plot(hist.history['accuracy'], color='blue', label='train')
        plt.plot(hist.history['val_accuracy'], color='orange', label='test')

        plt.savefig(model_name + '_statistics.png')
        plt.close()

    def predict(self, folder_name, model):
        self.model = model
        images = []

        for img_name in os.listdir(folder_name):
            img = image.load_img(os.path.join(folder_name, img_name), target_size=(
                self.IMG_HEIGHT, self.IMG_WIDTH))
            x = image.img_to_array(img) / 255
            x = np.expand_dims(x, axis=0)
            images.append(x)

        images = np.vstack(images)

        return self.model.predict(images)

    def predict_single(self, img_path, model):
        self.model = model

        img = image.load_img(img_path, target_size=(self.IMG_HEIGHT, self.IMG_WIDTH))
        x = image.img_to_array(img) / 255
        x = np.expand_dims(x, axis=0)

        images = np.vstack([ x ])

        return self.model.predict(images)[0]