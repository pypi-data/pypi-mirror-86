import keras
from keras.optimizers import SGD
from keras.utils import to_categorical
from keras.models import Sequential
from keras.layers import Conv2D, BatchNormalization
from keras.layers import MaxPooling2D, GlobalAveragePooling2D
from keras.layers import Dense
from keras.layers import Flatten
from keras.optimizers import SGD

bnmomemtum=0.9

def fire(x, squeeze, expand):
    y  = Conv2D(filters=squeeze, kernel_size=1, activation='relu', padding='same')(x)
    y = BatchNormalization(momentum=bnmomemtum)(y)
    y1 = Conv2D(filters=expand//2, kernel_size=1, activation='relu', padding='same')(y)
    y1 = BatchNormalization(momentum=bnmomemtum)(y1)
    y3 = Conv2D(filters=expand//2, kernel_size=3, activation='relu', padding='same')(y)
    y3 = BatchNormalization(momentum=bnmomemtum)(y3)
    return keras.layers.concatenate([y1, y3])

def fire_module(squeeze, expand):
    return lambda x: fire(x, squeeze, expand)

def get_model(num_classes):
    x = keras.layers.Input(shape=(192, 192, 3))

    y = Conv2D(kernel_size=3, filters=32, padding='same', use_bias=True, activation='relu')(x)
    y = BatchNormalization(momentum=bnmomemtum)(y)
    y = fire_module(24, 48)(y)
    y = MaxPooling2D(pool_size=2)(y)
    y = fire_module(48, 96)(y)
    y = MaxPooling2D(pool_size=2)(y)
    y = fire_module(64, 128)(y)
    y = MaxPooling2D(pool_size=2)(y)
    y = fire_module(48, 96)(y)
    y = MaxPooling2D(pool_size=2)(y)
    y = fire_module(24, 48)(y)
    y = GlobalAveragePooling2D()(y)
    y = Dense(num_classes, activation='softmax')(y)

    return keras.Model(x, y)
