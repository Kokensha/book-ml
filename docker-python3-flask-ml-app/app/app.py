# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
#
#
import base64
import os
import re as regexp
from pathlib import Path

import cv2
import numpy as np
from chainer_dogscats import dogscatsPredict
from chainer_mnist import mnistPredict
from flask import Flask, jsonify, redirect, render_template, request
from flask_cors import CORS
from keras_mnist import kerasPredict
from tensorflow_flower import flowerPredict

# -----------------------------------------------------------------------------
#
# アップロードするファイルの保存フォルダ
UPLOAD_FOLDER = './images'
# 許可するファイルのフォーマットの拡張子
ALLOWED_EXTENSIONS = {'jpg', 'jpeg'}
app = Flask(__name__)
app.secret_key = 'secret key for machine learning'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
CORS(app)


# =============================================================================
# ホーム
# -----------------------------------------------------------------------------
#

# -----------------------------------------------------------------------------
#
#
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        return jsonify({'result': ''})
    else:
        return render_template('index.html')


# =============================================================================
# Chainer MNIST
# -----------------------------------------------------------------------------
#

# -----------------------------------------------------------------------------
#
#
@app.route('/chainer', methods=['GET', 'POST'])
def chainer():
    if request.method == 'POST':
        result = getAnswerFromChainer(request)
        return jsonify({'result': result})
    else:
        return render_template('chainer.html')


# -----------------------------------------------------------------------------
# 判定結果を取得します
#
def getAnswerFromChainer(req):
    prepared_image = prepareImage(req)
    result = mnistPredict.result(prepared_image)
    return result


# =============================================================================
# Chainer Dogs & Cats
# -----------------------------------------------------------------------------
#

# -----------------------------------------------------------------------------
#
#
@app.route('/dogscats', methods=['GET', 'POST'])
def dogscats():
    if request.method == 'POST':
        result = getAnswerDogsCats(request)
        return jsonify({'result': result})
    else:
        return render_template('dogscats.html')


# -----------------------------------------------------------------------------
# 犬か猫か
#
def getAnswerDogsCats(req):
    prepareDogscatsImage(req)
    result = dogscatsPredict.result()
    return result


# -----------------------------------------------------------------------------
#
#
def prepareDogscatsImage(req):
    #
    image_string = regexp.search(r'base64,(.*)', req.form['image']).group(1)
    nparray = np.fromstring(base64.b64decode(image_string), np.uint8)
    image_src = cv2.imdecode(nparray, cv2.IMREAD_COLOR)
    cv2.imwrite('images/dogscats.jpg', image_src)


# =============================================================================
# Chainer Dogs & Cats 写真アップロード判別
# -----------------------------------------------------------------------------
#


# -----------------------------------------------------------------------------
# 犬か猫の画像ファイルをアップロードするだけ(結果は返さない)
#
@app.route('/dogscatsupload', methods=['GET', 'POST'])
def upload_file_dogscats():
    return upload_and_save_file(request, 'dogscats_upload.html', 'dogscats.jpg')


# -----------------------------------------------------------------------------
# アップロードした犬か猫の画像を判別する結果を取得します
#
@app.route('/dogscatsuploadresult', methods=['GET', 'POST'])
def dogscatsUploadResult():
    if request.method == 'GET':
        result = getUploadedDogscatsResult()
        return jsonify({'result': result})
    else:
        return render_template('dogscats_upload.html')


# -----------------------------------------------------------------------------
# 判定結果を取得します
#
def getUploadedDogscatsResult():
    result = dogscatsPredict.result()
    return result


# =============================================================================
# Keras MNIST
# -----------------------------------------------------------------------------
#

# -----------------------------------------------------------------------------
#
#
@app.route('/keras', methods=['GET', 'POST'])
def keras():
    if request.method == 'POST':
        result = getAnswerFromKeras(request)
        return jsonify({'result': result})
    else:
        return render_template('keras.html')


# -----------------------------------------------------------------------------
# 判定結果を取得します
#
def getAnswerFromKeras(req):
    prepared_image = prepareImage(req)
    result = kerasPredict.result(prepared_image)
    return result


# =============================================================================
# TensorFlow Flower 手書き判別
# -----------------------------------------------------------------------------
#

# -----------------------------------------------------------------------------
#
#
@app.route('/flower', methods=['GET', 'POST'])
def flower():
    if request.method == 'POST':
        result = getAnswerFromFlower(request)
        return jsonify({'result': result})
    else:
        return render_template('flower.html')


# -----------------------------------------------------------------------------
# 判定結果を取得します
#
def getAnswerFromFlower(req):
    image = prepareFlowerImage(req)
    result = flowerPredict.result(image)
    return result


# -----------------------------------------------------------------------------
#
#
def prepareFlowerImage(req):
    #
    image_string = regexp.search(r'base64,(.*)', req.form['image']).group(1)
    nparray = np.fromstring(base64.b64decode(image_string), np.uint8)
    image_src = cv2.imdecode(nparray, cv2.IMREAD_COLOR)
    cv2.imwrite('images/flower.jpg', image_src)
    return image_src


# =============================================================================
# TensorFlow Flower 写真アップロード判別
# -----------------------------------------------------------------------------
#


# -----------------------------------------------------------------------------
# 画像ファイルをアップロードするだけ(結果は返さない)
#
@app.route('/flowerupload', methods=['GET', 'POST'])
def upload_file_flower():
    return upload_and_save_file(request, 'flower_upload.html', 'flower.jpg')


# -----------------------------------------------------------------------------
# アップロードした花の画像を判別する結果を取得します
#
@app.route('/floweruploadresult', methods=['GET', 'POST'])
def flowerUploadResult():
    if request.method == 'GET':
        result = getUploadedFlowerResult()
        return jsonify({'result': result})
    else:
        return render_template('flower_upload.html')


# -----------------------------------------------------------------------------
# 判定結果を取得します
#
def getUploadedFlowerResult():
    result = flowerPredict.result('')
    return result


# =============================================================================
# ここから共通処理
# -----------------------------------------------------------------------------
#

# -----------------------------------------------------------------------------
# 入力イメージを処理しておく関数(Chainer MNIST, Keras MNIST共通)
#
def prepareImage(req):
    image_result = None
    image_string = regexp.search(r'base64,(.*)', req.form['image']).group(1)
    nparray = np.fromstring(base64.b64decode(image_string), np.uint8)
    image_nparray = cv2.imdecode(nparray, cv2.IMREAD_COLOR)
    # 画像を学習データのように黒い背景、白い文字に変換します
    image_nega = 255 - image_nparray
    # グレースケールに変換します
    image_gray = cv2.cvtColor(image_nega, cv2.COLOR_BGR2GRAY)
    image_result = cv2.resize(image_gray, (28, 28))
    cv2.imwrite('images/mnist_number.jpg', image_result)
    return image_result


# -----------------------------------------------------------------------------
# 許可しているファイルフォーマットかどうかの判定
#
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() \
           in ALLOWED_EXTENSIONS


# -----------------------------------------------------------------------------
# クライアント側から送られたファイルを保存した上、指定したテンプレートに移動します
#
def upload_and_save_file(request, template_name, save_file_name):
    if request.method == 'POST':
        # リクエストオブジェクトに指定したファイルが存在しなければ、
        if 'from_client_file' not in request.files:
            print('ファイルパーツがない')
            return redirect(request.url)

        # ファイルが存在している場合
        file = request.files['from_client_file']
        # ファイル名が空の場合
        if file.filename == '':
            print('ファイル選択していない')
            return redirect(request.url)

        # ファイルが存在し、かつ許可されたファイルフォーマットであれば指定した場所と指定した名称で保存します
        if file and allowed_file(file.filename):
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], save_file_name))

        return render_template(template_name)
    else:
        return render_template(template_name)


# -----------------------------------------------------------------------------
# 手書き用Canvasをクリアします
#
@app.route('/clearcanvas', methods=['GET', 'POST'])
def clearcanvas():
    if request.method == 'POST':
        # 既存のファイルを一旦削除します
        for p in Path('./images').glob('*.jpg'):
            p.unlink()
        return jsonify({'status': 'OK'})
    else:
        return render_template('index.html')


# =============================================================================
# サーバーを起動すします
# -----------------------------------------------------------------------------
#

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5000)
