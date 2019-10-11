
import numpy as np
import tensorflow as tf
from tensorflow.keras.layers import Layer

class CropResizedGradientLayer(Layer):
    """Basic resize layer for self driving model"""
    def __init__(self, box, crop_size, horizontal=False, name='crop_and_resize_layer', **kwargs):
        super(CropResizedGradientLayer, self).__init__(name=name, **kwargs)
        self.horizontal = horizontal
        self.box = box
        self.crop_size = crop_size

    def call(self, x):
        box = self.box
        x = tf.image.crop_to_bounding_box(x, box[0], box[1], box[2], box[3])
        x = tf.image.resize_images(x, self.crop_size)
        v, h = tf.image.image_gradients(x)
        if self.horizontal:
            x = h
        else:
            x = v
        return x

class Predictor:
    def __init__(self, model_path, classes_num):
        self.model = tf.keras.models.load_model(model_path)
        self.classes_num = classes_num

    def call(self, frame):
        prediction = self.model.predict(frame.reshape((-1,) + frame.shape))
        return np.argmax(prediction[0]) / self.classes_num
