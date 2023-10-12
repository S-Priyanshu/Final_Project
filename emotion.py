import os

import tensorflow as tf

import keras
from keras.engine.saving import load_model
from keras.models import Sequential
from keras.layers import Conv2D, MaxPooling2D, AveragePooling2D
from keras.layers import Dense, Activation, Dropout, Flatten

from keras.preprocessing import image
from keras.preprocessing.image import ImageDataGenerator

import numpy as np
# def train():
#     #------------------------------
#     sess = tf.Session()
#     keras.backend.set_session(sess)
#     #------------------------------
#     #variables
#     num_classes = 7 #angry, disgust, fear, happy, sad, surprise, neutral
#     batch_size = 256
#     epochs = 35
#     #------------------------------
#
#     with open(r"C:\Users\USER\PycharmProjects\mental_health\static\fer2013.csv") as f:
#         content = f.readlines()
#
#
#
#
#     ###############################################
#     lines = np.array(content)
#
#     no_instances = lines.size
#
#     #------------------------------
#     #initialize trainset and test set
#     x_train, y_train, x_test, y_test = [], [], [], []
#     #
#     # #------------------------------
#     # #transfer train and test set data
#     for i in range(1,no_instances):
#         try:
#             emotion, img, usage = lines[i].split(",")
#
#             val = img.split(" ")
#
#             pixels = np.array(val, 'float32')
#
#             emotion = keras.utils.to_categorical(emotion, num_classes)
#
#             if 'Training' in usage:
#                 y_train.append(emotion)
#                 x_train.append(pixels)
#             elif 'PublicTest' in usage:
#                 y_test.append(emotion)
#                 x_test.append(pixels)
#         except:
#             pass
#
#     #------------------------------
#     #data transformation for train and test sets
#     x_train = np.array(x_train, 'float32')
#     y_train = np.array(y_train, 'float32')
#     x_test = np.array(x_test, 'float32')
#     y_test = np.array(y_test, 'float32')
#
#     x_train /= 255 #normalize inputs between [0, 1]
#     x_test /= 255
#
#     x_train = x_train.reshape(x_train.shape[0], 48, 48, 1)
#     x_train = x_train.astype('float32')
#     x_test = x_test.reshape(x_test.shape[0], 48, 48, 1)
#     x_test = x_test.astype('float32')
#
#     print(x_train.shape[0], 'train samples')
#     print(x_test.shape[0], 'test samples')
#     #------------------------------
#     #construct CNN structure
#     model = Sequential()
#
#     #1st convolution layer
#     model.add(Conv2D(64, (5, 5), activation='relu', input_shape=(48,48,1)))
#     model.add(MaxPooling2D(pool_size=(5,5), strides=(2, 2)))
#
#     #2nd convolution layer
#     model.add(Conv2D(64, (3, 3), activation='relu'))
#     model.add(Conv2D(64, (3, 3), activation='relu'))
#     model.add(AveragePooling2D(pool_size=(3,3), strides=(2, 2)))
#
#     #3rd convolution layer
#     model.add(Conv2D(128, (3, 3), activation='relu'))
#     model.add(Conv2D(128, (3, 3), activation='relu'))
#     model.add(AveragePooling2D(pool_size=(3,3), strides=(2, 2)))
#
#     model.add(Flatten())
#
#     #fully connected neural networks
#     model.add(Dense(1024, activation='relu'))
#     model.add(Dropout(0.2))
#     model.add(Dense(1024, activation='relu'))
#     model.add(Dropout(0.2))
#
#     model.add(Dense(num_classes, activation='softmax'))
#     #------------------------------
#     #batch process
#     gen = ImageDataGenerator()
#     train_generator = gen.flow(x_train, y_train, batch_size=batch_size)
#
#     #------------------------------
#
#     model.compile(loss='categorical_crossentropy'
#         , optimizer=keras.optimizers.Adam()
#         , metrics=['accuracy']
#     )
#
#     #------------------------------
#
#     if  not os.path.exists("model.h5"):
#
#         model.fit_generator(train_generator, steps_per_epoch=batch_size, epochs=epochs)
#         model.save("model.h5")#train for randomly selected one
#     else:
#         model=load_model("model.h5") #load weights


def predict(filename):

    img = image.load_img(filename, grayscale=True, target_size=(48, 48))

    x = image.img_to_array(img)
    x = np.expand_dims(x, axis = 0)
    print(x,"eeeeee")
    x /= 255
    model=load_model(r"C:\Users\USER\PycharmProjects\mental_new\Mental_Health\model.h5", compile=False) #load weights
    result = model.predict(x)

    max_index = np.argmax(result[0])
    emotions = ('angry', 'disgust', 'fear', 'happy', 'sad', 'surprise', 'neutral')
    print(result[0])
    emotion = emotions[max_index]
    print(emotion,"rrrrrrr")
    return emotion

    #------------------------------


# predict(r"D:\Workspace\2022-2023\LBS\Mental_Health\static\sad.jpg")