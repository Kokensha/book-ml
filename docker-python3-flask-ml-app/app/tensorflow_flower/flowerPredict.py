#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright 2017 The TensorFlow Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================


#
# このファイルはTensorFlowのGitHubでApache License 2.0で公開したプログラムを改造したものです。
# 元のファイルはこちらです：https://github.com/tensorflow/tensorflow/blob/master/tensorflow/examples/label_image/label_image.py
#
from __future__ import absolute_import, division, print_function

import os

import numpy as np
import tensorflow as tf


def load_graph(model_file):
    graph = tf.Graph()
    graph_def = tf.GraphDef()

    with open(model_file, 'rb') as f:
        graph_def.ParseFromString(f.read())
    with graph.as_default():
        tf.import_graph_def(graph_def)

    return graph


def load_labels(label_file):
    label = []
    proto_as_ascii_lines = tf.gfile.GFile(label_file).readlines()
    for l in proto_as_ascii_lines:
        label.append(l.rstrip())
    return label


# 学習済モデルをロードします
model_file = os.path.abspath(os.path.dirname(__file__)) + '/output_graph.pb'
label_file = os.path.abspath(os.path.dirname(__file__)) + '/output_labels.txt'
graph = load_graph(model_file)
labels = load_labels(label_file)
print('TensorFlow Flower model is loaded.')


def read_tensor_from_image_file(
        file_name,
        input_height=299,
        input_width=299,
        input_mean=0,
        input_std=255,
):
    input_name = 'file_reader'
    # output_name = 'normalized'
    file_reader = tf.read_file(file_name, input_name)
    # このプログラムではjpgフォーマットのファイル限定になります。
    image_reader = tf.image.decode_jpeg(
        file_reader, channels=3, name='jpeg_reader')
    float_caster = tf.cast(image_reader, tf.float32)
    dims_expander = tf.expand_dims(float_caster, 0)
    resized = tf.image.resize_bilinear(dims_expander,
                                       [input_height, input_width])
    normalized = tf.divide(tf.subtract(resized, [input_mean]), [input_std])
    sess = tf.Session()
    result = sess.run(normalized)

    return result


def result(input_data):
    file_name = './images/flower.jpg'
    input_height = 299
    input_width = 299
    input_mean = 0
    input_std = 255
    input_layer = "Placeholder"
    output_layer = "final_result"

    t = read_tensor_from_image_file(
        file_name,
        input_height=input_height,
        input_width=input_width,
        input_mean=input_mean,
        input_std=input_std)

    input_name = 'import/' + input_layer
    output_name = 'import/' + output_layer
    #
    input_operation = graph.get_operation_by_name(input_name)
    output_operation = graph.get_operation_by_name(output_name)

    with tf.Session(graph=graph) as sess:
        results = sess.run(output_operation.outputs[0],
                           {input_operation.outputs[0]: t})
    results = np.squeeze(results)

    top_k = results.argsort()[-5:][::-1]

    tmpTop = 0
    result_label = ''
    for i in top_k:
        if tmpTop < results[i]:
            tmpTop = results[i]
            result_label = labels[i]

        print(labels[i], results[i])

        return result_label
