# coding: utf-8


import os
import sys
import urllib3

from cafebot import settings
from cafebot.gnavi import Gnavi
from flask import Flask, request, abort
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
    SourceUser, SourceGroup, SourceRoom,
    TemplateSendMessage, ConfirmTemplate, MessageTemplateAction,
    ButtonsTemplate, ImageCarouselTemplate, ImageCarouselColumn, URITemplateAction,
    CarouselTemplate, CarouselColumn, LocationMessage, LocationSendMessage,
)

app = Flask(__name__)
line_bot_api = settings.line_bot_api
handler = settings.handler
static_tmp_path = settings.static_tmp_path

class Bot(object):
    def __init__(self):
        gnavi = Gnavi(settings.gnavi_key, event)
        gnavi_data = gnavi.gnavi()
        self.shop_name = gnavi_data['name']
        self.shop_address = gnavi_data['address']
        self.destatitude = gnavi_data['Latitude']
        self.deestLongitude = gnavi_data['Longitude']
        self.shop_image = gnavi_data['shop_image1']

    def run(self):
        port = int(os.getenv("PORT", 5000))
        # # create tmp dir for download content
        make_static_tmp_dir()
        app.run(host="0.0.0.0", port=port)

    # function for create tmp dir for download content
    def make_static_tmp_dir(self):
        try:
            os.makedirs(static_tmp_path)
        except OSError as exc:
            if exc.errno == errno.EEXIST and os.path.isdir(static_tmp_path):
                pass
            else:
                raise

    @app.route("/callback", methods=['POST'])
    def callback(self):
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
    def handle_location_message(self, event):
        destLatitude = str(self.destatitude)
        destLongitude = str(self.deestLongitude)
        route_url = 'http://maps.google.com/maps'\
                    + '?saddr=' + self.srcLatitude + ',' + self.srcLongitude\
                    + '&daddr=' + destLatitude + ',' + destLongitude\
                    + '&dirflg=w'
        buttons_template = ButtonsTemplate(
            title=self.shop_name, text='ここからのルートを表示します', actions=[
                URITemplateAction(
                    label='ルートを表示', uri=route_url),
            ])
        template_message = TemplateSendMessage(
            alt_text='Buttons', template=buttons_template)
        line_bot_api.reply_message(event.reply_token, template_message)
