# -*- coding: utf-8 -*-

import time

import cv2
from picamera import PiCamera
from picamera.array import PiRGBArray

# フレームサイズ
FRAME_W = 320
FRAME_H = 240

# 顔検出用カスケー分類器
cascadeFilePath = '/usr/local/share/OpenCV/lbpcascades/lbpcascade_frontalface.xml'
# 分類器をセットします
frontalFaceCascadeClf = cv2.CascadeClassifier(cascadeFilePath)

# カメラインスタンス作成
v_camera = PiCamera()
# カメラの解像度を設定します
v_camera.resolution = (FRAME_W, FRAME_H)
# カメラのフレームレートを設定します(FPS)
v_camera.framerate = 16
# v_cameraインスタンスから、画像のRGB配列取得します。そのままnumpyで処理できます
rawCapture = PiRGBArray(v_camera, size=(FRAME_W, FRAME_H))
# timeモジュールのsleep関数です。ここでは1秒待ちます
time.sleep(1)

# v_camera.capture_continuousは明示的に停止指示があるまで、無限にイメージを取得し続けます
for raw_camera_data in v_camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    # 画像を配列データを変数frameに代入します
    frame = raw_camera_data.array
    # 取得したBGRデータをグレースケールに変換します。
    gray_image = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # グレースケールイメージに変換します
    gray_image = cv2.equalizeHist(gray_image)
    # 顔検出
    multipleFaces = frontalFaceCascadeClf.detectMultiScale(gray_image, 1.1, 3, 0, (20, 20))
    # 線の色
    line_color = (255, 102, 51)
    # 文字の色
    font_color = (255, 102, 51)
    # 検出した顔に枠を書く
    for (x, y, width, height) in multipleFaces:
        # 見つかった顔を線で囲みます
        cv2.rectangle(frame, (x, y), (x + width, y + height), line_color, 2)
        # 顔の上に「FACE」という文字を表示します
        cv2.putText(frame, 'FACE', (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.7, font_color, 1, cv2.LINE_AA)

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
