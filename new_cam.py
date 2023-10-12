
import numpy as np


from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, Flatten
from tensorflow.keras.layers import Conv2D
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.layers import MaxPooling2D
from tensorflow.keras.preprocessing.image import ImageDataGenerator
import os

attendence_pic_path=r"C:\Users\USER\PycharmProjects\mental_new\Mental_Health\static\\"

def start_camera():
    while True:
        try:
            import cv2

            print("fir")
            webcam = cv2.VideoCapture(0)
            key = cv2.waitKey(1)


            check, frame = webcam.read()

            import time

            filename = "y22.jpg"
            cv2.imwrite(attendence_pic_path + filename, img=frame)
            webcam.release()
            # img_new = cv2.imread('saved_img.jpg', cv2.IMREAD_GRAYSCALE)
            # img_new = cv2.imshow("Captured Image", img_new)
            cv2.waitKey(1650)
            cv2.destroyAllWindows()
            print("Processing image...")
            img_ = cv2.imread(attendence_pic_path + filename, cv2.IMREAD_ANYCOLOR)
            print("Converting RGB image to grayscale...")
            gray = cv2.cvtColor(img_, cv2.COLOR_BGR2GRAY)
            print("Converted RGB image to grayscale...")
            print("Resizing image to 28x28 scale...")
            img_ = cv2.resize(gray, (28, 28))
            print("Resized...")
            img_resized = cv2.imwrite(filename=attendence_pic_path + 'saved_img-final.jpg', img=img_)
            print("Image saved!")
            webcam.release()
            cv2.destroyAllWindows()

            from emotion import predict
            res=predict(attendence_pic_path + 'saved_img-final.jpg')
            print("Result : ", res)
            return res

        except(KeyboardInterrupt):
            print("Turning off camera.")
            webcam.release()
            print("Camera off.")
            print("Program ended.")
            cv2.destroyAllWindows()
            # break


# start_camera()