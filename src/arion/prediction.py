
import numpy as np
import tensorflow as tf
from tensorflow.keras.layers import Layer

class Predictor:
    def __init__(self, model_path, classes_num):
        self.model = tf.keras.models.load_model(model_path)
        self.classes_num = classes_num

    def call(self, frame):
        prediction = self.model.predict(frame.reshape((-1,) + frame.shape))
        p = np.argmax(prediction[0]) / self.classes_num
        p = (p * 2) - 1
        return p
