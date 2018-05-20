# coding: utf-8

import os
import sys
import urllib3
import json

def gnavi_settings():
    # APIアクセスキー
    keyid = "023aa91a40b3e48911c22771036dda7f"
    # エンドポイントURL
    url = "https://api.gnavi.co.jp/RestSearchAPI/20150630/"
    # 緯度・経度、範囲を変数に入れる
    # 緯度経度は日本測地系で日比谷シャンテのもの。範囲はrange=1で300m以内を指定している。
    # 緯度
    latitude = "35.670083"
    # 経度
    longitude = "139.763267"
    # 範囲
    range = "1"

    ####
    # APIアクセス
    ####
    # URLに続けて入れるパラメータを組立
    query = [
        ("format", "json"),
        ("keyid", keyid),
        ("latitude", latitude),
        ("longitude", longitude),
        ("range", range)
    ]

    # URL生成
    url += "?{0}".format(urllib3.urlencode(query))
