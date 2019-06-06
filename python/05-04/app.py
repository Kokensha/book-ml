#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time

import cv2
import garbageDetector as detector
from PIL import Image
from picamera import PiCamera
from picamera.array import PiRGBArray

# フレームサイズ
FRAME_W = 320
FRAME_H = 320

# カメラインスタンス作成
v_camera = PiCamera()
# カメラの解像度を設定します
v_camera.resolution = (FRAME_W, FRAME_H)
# カメラのフレームレートを設定します(FPS)
v_camera.framerate = 1
# v_cameraインスタンスから、画像のRGB配列取得します。そのままnumpyで処理できます
rawCapture = PiRGBArray(v_camera, size=(FRAME_W, FRAME_H))
# timeモジュールのsleep関数です。ここでは1秒待ちます
time.sleep(1)

# v_camera.capture_continuousは明示的に停止指示があるまで、無限にイメージを取得し続けます
for raw_camera_data in v_camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):

    # 画像を配列データを変数frameに代入します
    frame = raw_camera_data.array
    # RGBデータに変換します
    image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    #
    PIL_data = Image.fromarray(image_rgb)

    detector.result(PIL_data)

    # ビデオに表示
    cv2.imshow('Video', frame)
    # キーボードの入力を処理します
    key = cv2.waitKey(1) & 0xFF
    rawCapture.truncate(0)
    # [q]キーと入力すると、プログラムを終了させます
    if key == ord("q"):
        break
# 終了処理、プログラムが作ったウィンドウを全部閉じます
cv2.destroyAllWindows()
