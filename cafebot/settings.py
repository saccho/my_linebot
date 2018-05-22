# coding: utf-8

from __future__ import unicode_literals

import errno
import os
import sys
import urllib3

from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
    SourceUser, SourceGroup, SourceRoom,
    TemplateSendMessage, ConfirmTemplate, MessageTemplateAction,
    ButtonsTemplate, ImageCarouselTemplate, ImageCarouselColumn, URITemplateAction,
    CarouselTemplate, CarouselColumn, LocationMessage, LocationSendMessage,
)

# get channel_secret and channel_access_token from your environment variable
channel_secret = os.getenv('LINE_CHANNEL_SECRET', None)
channel_access_token = os.getenv('LINE_CHANNEL_ACCESS_TOKEN', None)
if channel_secret is None:
    print('Specify LINE_CHANNEL_SECRET as environment variable.')
    sys.exit(1)
if channel_access_token is None:
    print('Specify LINE_CHANNEL_ACCESS_TOKEN as environment variable.')
    sys.exit(1)

line_bot_api = LineBotApi(channel_access_token)
handler = WebhookHandler(channel_secret)

static_tmp_path = os.path.join(os.path.dirname(__file__), 'static', 'tmp')

# # function for create tmp dir for download content
# def make_static_tmp_dir():
#     try:
#         os.makedirs(static_tmp_path)
#     except OSError as exc:
#         if exc.errno == errno.EEXIST and os.path.isdir(static_tmp_path):
#             pass
#         else:
#             raise


'''
gnavi config
'''
# APIアクセスキー
gnavi_key = "023aa91a40b3e48911c22771036dda7f"
# エンドポイントURL
url = "https://api.gnavi.co.jp/RestSearchAPI/20150630/"
# 緯度・経度、範囲を変数に入れる
# 緯度経度は日本測地系で日比谷シャンテのもの。範囲はrange=1で300m以内を指定している。
# 緯度
latitude = str(event.message.latitude)
# 経度
longitude = str(event.message.longitude)
# 範囲
range = "1"

####
# APIアクセス
####
# URLに続けて入れるパラメータを組立
query = [
    ("format", "json"),
    ("keyid", gnavi_key),
    ("latitude", latitude),
    ("longitude", longitude),
    ("range", range)
]

# URL生成
gnavi_url += "?{0}".format(urllib3.urlencode(query))
