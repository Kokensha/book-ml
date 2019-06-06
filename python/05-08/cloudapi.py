#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests

# API Key
subscription_key = "xxxxxxxxx"
assert subscription_key
# あなたが利用している api endpoint
vision_base_url = "https://japaneast.api.cognitive.microsoft.com/vision/v2.0/"


# 画像のキャプションを取得する関数


def getImageCaption(image_url):
    analyze_url = vision_base_url + "analyze"
    headers = {'Ocp-Apim-Subscription-Key': subscription_key}
    params = {'visualFeatures': 'Categories,Description,Color'}
    data = {'url': image_url}
    response = requests.post(analyze_url, headers=headers, params=params, json=data)
    response.raise_for_status()
    analysis = response.json()
    image_caption = analysis["description"]["captions"][0]["text"].capitalize()
    return image_caption


# 写真url指定

# image_url = "https://kokensha.xyz/wp-content/uploads/2018/05/IMG_5338_small-768x576.png"

image_url = "https://kokensha.xyz/wp-content/uploads/2018/03/IMG_0903_small-768x512.jpg"

# 結果表示

print(getImageCaption(image_url))
