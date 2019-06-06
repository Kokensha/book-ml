# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
#
#
import os

import chainer
import chainer.functions as F
import chainer.links as L
from chainer import serializers


# -----------------------------------------------------------------------------
#
# 学習モデルの定義
class MLP(chainer.Chain):
    def __init__(self, number_hidden_units=1000, number_out_units=10):
        # 親クラスのコンストラクタを呼び出し、必要な初期化を行います。
        super(MLP, self).__init__()
        #
        with self.init_scope():
            self.layer1 = L.Linear(None, number_hidden_units)
            self.layer2 = L.Linear(number_hidden_units, number_hidden_units)
            self.layer3 = L.Linear(number_hidden_units, number_out_units)

    def __call__(self, input_data):
        #
        result1 = F.relu(self.layer1(input_data))
        result2 = F.relu(self.layer2(result1))
        return self.layer3(result2)


# 学習済みモデル
chainer_mnist_model = MLP()
serializers.load_npz(
    os.path.abspath(os.path.dirname(__file__)) + '/chainer-mnist.model',
    chainer_mnist_model)
print('Chainer MNIST model is loaded.')


def result(input_image_data):
    # print('渡された画像データ\n')
    # print(input_image_data)
    # print('\n')

    input_image_data = input_image_data.astype('float32')
    input_image_data = input_image_data.reshape(1, 28 * 28)
    # print('配列形状変換\n')
    # print(input_image_data)
    # print('\n')

    input_image_data = input_image_data / 255
    # print('255で割ります\n')
    # print(input_image_data)
    # print('\n')

    input_image_data = input_image_data[None, ...]
    # print('ミニバッチの形状に\n')
    # print(input_image_data)
    # print('\n')

    # input_image_data = chainer_mnist_model.xp.asarray(input_image_data)
    predict = chainer_mnist_model(input_image_data)
    result = predict.array
    probable_label = result.argmax(axis=1)

    # print('モデルの判定結果\n')
    # print(result)
    # print('\n')

    print('最終結果\n')
    print(probable_label[0])
    print('\n')

    return str(probable_label[0])
