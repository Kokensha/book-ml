# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
#
#
import os

import chainer
import chainer.functions as F
import chainer.links as L
import numpy as np
from PIL import Image
from chainer import Chain, serializers
from chainer.cuda import to_cpu

# -----------------------------------------------------------------------------
#
INPUT_WIDTH = 128
INPUT_HEIGHT = 128


# 学習モデルの定義
class CNN(Chain):
    # コンストラクタ
    def __init__(self):
        super(CNN, self).__init__()

        with self.init_scope():
            self.conv1 = L.Convolution2D(
                None, out_channels=32, ksize=3, stride=1, pad=1)
            self.conv2 = L.Convolution2D(
                in_channels=32, out_channels=64, ksize=3, stride=1, pad=1)
            self.conv3 = L.Convolution2D(
                in_channels=64, out_channels=128, ksize=3, stride=1, pad=1)
            self.conv4 = L.Convolution2D(
                in_channels=128, out_channels=256, ksize=3, stride=1, pad=1)
            self.layer1 = L.Linear(None, 1000)
            self.layer2 = L.Linear(1000, 2)

    #
    def __call__(self, input):
        func = F.max_pooling_2d(F.relu(self.conv1(input)), ksize=2, stride=2)
        func = F.max_pooling_2d(F.relu(self.conv2(func)), ksize=2, stride=2)
        func = F.max_pooling_2d(F.relu(self.conv3(func)), ksize=2, stride=2)
        func = F.max_pooling_2d(F.relu(self.conv4(func)), ksize=2, stride=2)
        func = F.dropout(F.relu(self.layer1(func)), ratio=0.80)
        func = self.layer2(func)
        return func


# 学習済みモデル
chainer_dogscats_model = L.Classifier(CNN())
# 学習済みモデルファイル：chainer-dogscats-model.h5はJupyter Notebookで作成して
# このファイルと同じフォルダに配置してください。
serializers.load_hdf5(
    os.path.abspath(os.path.dirname(__file__)) + '/chainer-dogscats-model.h5',
    chainer_dogscats_model)

print('Chainer Dogs & Cats model is loaded.')


#
def data_reshape(image_data):
    image_array = np.array(image_data)
    return image_array.transpose(2, 0, 1)


def convert_test_data(image_file_path, size, show=False):
    image = Image.open(image_file_path)

    # 共通の画像のリサイズ処理です。第5章の１番目のレシピを参照してください
    result_image = image.resize((INPUT_WIDTH, INPUT_HEIGHT), Image.LANCZOS)

    # 画像データをChainerのConvolution2Dに使えるように整備します
    image = data_reshape(result_image)

    # 型をfloat32に変換します
    result = image.astype(np.float32)
    # 学習済みモデルに渡します
    result = chainer_dogscats_model.xp.asarray(result)
    #
    result = result[None, ...]
    return result


def result():
    retval = ''
    file_name = './images/dogscats.jpg'
    # 学習時と同じ画像のサイズにしなければいけません

    test_data = convert_test_data(file_name, (INPUT_WIDTH, INPUT_HEIGHT))
    with chainer.using_config('train', False), chainer.using_config(
            'enable_backprop', False):
        test_teacher_labels = chainer_dogscats_model.predictor(test_data)
        test_teacher_labels = to_cpu(test_teacher_labels.array)
        test_teacher_label = test_teacher_labels.argmax(axis=1)[0]
        if test_teacher_label == 0:
            retval = '猫'
        else:
            retval = '犬'

    return retval
