# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
#
#
import os

import numpy as np
from keras import backend as Keras
from keras.models import load_model

# -----------------------------------------------------------------------------
#
Keras.clear_session()
# 学習済みモデル
keras_mnist_model = load_model(
    os.path.abspath(os.path.dirname(__file__)) + '/keras-mnist-model.h5')

keras_mnist_model._make_predict_function()
keras_mnist_model.summary()
print('Keras MNIST model is loaded.')


def result(input_data):
    input_data = np.expand_dims(input_data, axis=0)
    input_data = input_data.reshape(input_data.shape[0], 28, 28, 1)
    result = np.argmax(keras_mnist_model.predict(input_data))
    return int(result)
