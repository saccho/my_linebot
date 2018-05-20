# -*- coding: utf-8 -*-

#  Licensed under the Apache License, Version 2.0 (the "License"); you may
#  not use this file except in compliance with the License. You may obtain
#  a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#  WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#  License for the specific language governing permissions and limitations
#  under the License.

from __future__ import unicode_literals

import errno
import os
import sys
import tempfile
from argparse import ArgumentParser
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

app = Flask(__name__)

# # get channel_secret and channel_access_token from your environment variable
# channel_secret = os.getenv('LINE_CHANNEL_SECRET', None)
# channel_access_token = os.getenv('LINE_CHANNEL_ACCESS_TOKEN', None)
# if channel_secret is None:
#     print('Specify LINE_CHANNEL_SECRET as environment variable.')
#     sys.exit(1)
# if channel_access_token is None:
#     print('Specify LINE_CHANNEL_ACCESS_TOKEN as environment variable.')
#     sys.exit(1)
#
# line_bot_api = LineBotApi(channel_access_token)
# handler = WebhookHandler(channel_secret)
#
# static_tmp_path = os.path.join(os.path.dirname(__file__), 'static', 'tmp')
#
#
# # function for create tmp dir for download content
# def make_static_tmp_dir():
#     try:
#         os.makedirs(static_tmp_path)
#     except OSError as exc:
#         if exc.errno == errno.EEXIST and os.path.isdir(static_tmp_path):
#             pass
#         else:
#             raise


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

@handler.add(MessageEvent, message=LocationMessage)
def handle_location_message(event):
    address = event.message.address.split()
    srcLatitude = str(event.message.latitude)
    srcLongitude = str(event.message.longitude)
    destLatitude = '37.8670224'
    destLongitude = '138.9425633'
    route_url = 'http://maps.google.com/maps'\
                + '?saddr=' + srcLatitude + ',' + srcLongitude\
                + '&daddr=' + destLatitude + ',' + destLongitude\
                + '&dirflg=w'
    buttons_template = ButtonsTemplate(
        title='ルート', text='ここからのルートを表示します', actions=[
            URITemplateAction(
                label='ルートを表示', uri=route_url),
        ])
    template_message = TemplateSendMessage(
        alt_text='Buttons', template=buttons_template)
    line_bot_api.reply_message(event.reply_token, template_message)


if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    # create tmp dir for download content
    make_static_tmp_dir()
    app.run(host="0.0.0.0", port=port)
