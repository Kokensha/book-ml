# book-ml

このレポジトリは、書籍「今すぐ試したい！機械学習・深層学習（ディープラーニング）画像認識プログラミングレシピ」のソースコードを配布するレポジトリです。

アマゾンのリンクはこちらです：https://www.amazon.co.jp/dp/4798056839

<img src="book-ml.jpg" alt="book-ml" width="300">

<img src="book-ml_01.jpg" alt="book-ml" width="800">


# フォルダーの説明

* Colaboratory：本書で使うJupyter NoteBookです。Google Colaboratoryにインポートして実行してください。インポートする方法は本書の96ページをご参照ください。
* docker-python3-flask-ml-app：04-05 節、04-06 節、05-01節、05-03 節のサンプルコードと関連するウェブアプリケーションプログラムソースコード。PCの場合は```docker-compose up```で起動させることができます（Dockerが必要です）。詳しくは本書の267ページの「Column」の説明をご参照ください。
* python：04-02 節と05-04 節と05-08 節と07-02 節のPythonプログラムのソースコード
* scripts：04-02 節のコマンドなどをまとめたファイル

詳しくは、それぞれのフォルダの中身をご確認ください。

Pull Request歓迎！

著者のTwitter：https://twitter.com/kokensha_tech


# 注意事項

## ページ259

python3 app.pyをそのまま実行すると、学習済モデルファイルが見つからずに、正常に実行でできません。これはデータの権利の考慮のため、04-06の学習済モデルファイルをGitHubに配布していないのが原因です。

対応方法：270ページからの04-06節のレシピの手順を沿って、まず猫犬の認識用の学習済モデルファイルを作成して、手動で配置してください。

配置場所は book-ml/docker-python3-flask-ml-app/app/chainer_dogscats/ の配下です。

04-06で学習のために使用するデータは、下記のURL(Kaggle)から取得することが可能です（ユーザー登録が必要）。

* https://www.kaggle.com/c/dogs-vs-cats/data

* あるいは、動くバージョンをご参照ください。https://github.com/kawashimaken/docker-python3-flask-ml-app


# 訂正

## ページ108

一番下のOutputの日本語

誤：「False 花は薔薇ですね」

正：「False 花は薔薇ではないですね」

## ページ147、ページ148、ページ231

Pythonプログラムのimportのセクションに下記の一行が追記します（配布しているプログラムの方ではすでに含まれていますので、配布プログラムを利用する場合は、追加不要）。

```Python
from mpl_toolkits.mplot3d import Axes3D
```

## ページ173

新しいバージョンのopenCVを利用する読者に下記のエラーが発生するかもしれません。
```ValueError: not enough values to unpack (expected 3, got 2)```


次のコードのように修正して、正常に実行できます。
```Python
import numpy as np
import cv2
import matplotlib.pyplot as plt
 
img_bgr = cv2.imread('kawashima01.jpg')
img_gray = cv2.cvtColor(img_bgr,cv2.COLOR_BGR2GRAY)
retval,thresh = cv2.threshold(img_gray,88,255,0)

contours, hierarchy = cv2.findContours(thresh,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)

blank_image = 255 * np.ones((320,320,3), np.uint8)
result_img = cv2.drawContours(blank_image, contours, -1, (0,0,255), 3)
 
#
plt.imshow(result_img)
plt.show()
```

## ページ175

Pythonプログラム （配布しているプログラムの方は正しいプログラムになっております、配布プログラムを利用する場合は、修正不要）。

誤：x.shape[:2]

正：image.shape[:2]

## ページ226

誤：図1 scikit-learn MNIST手書きデータ

正：図1 scikit-learn 手書きデータ

誤：左側データのタイトル　iris.data/データ

正：左側データのタイトル　digits.data/データ

## 第５章　第３節（ページ：366）、第４節（ページ：379）　転移学習のColabについて

当時執筆時（2018年12月）、ColabのデフォルトのTensorFlowは当時の最新版1.xを使っていましたが、今はColabのデフォルトのTensorFlowのバージョンは2.xになっています。

当該転移学習のプログラムは、TensorFlow1.xのバージョンを使用する必要があります。
そのため、Colabの一番先頭で、TensorFlow1.xを利用すると宣言する必要があります。
Colabのプログラムの先頭に、下記を追加、実行する必要があります。

```
%tensorflow_version 1.x
```



# 本書の姉妹プロジェクト

## 機械学習・深層学習レッスン

https://github.com/Kokensha/machine_learning_deep_learning_lessons

## 川島のITスキルサロンのRepo

https://github.com/kawashimaken/salon
