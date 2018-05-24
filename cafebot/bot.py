# coding: utf-8


import os
import sys
import urllib3

# from cafebot import settings
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

channel_secret = os.getenv('LINE_CHANNEL_SECRET', None)
channel_access_token = os.getenv('LINE_CHANNEL_ACCESS_TOKEN', None)
gnavi_key = "023aa91a40b3e48911c22771036dda7f"

if channel_secret is None:
    print('Specify LINE_CHANNEL_SECRET as environment variable.')
    sys.exit(1)
if channel_access_token is None:
    print('Specify LINE_CHANNEL_ACCESS_TOKEN as environment variable.')
    sys.exit(1)

line_bot_api = LineBotApi(channel_access_token)
handler = WebhookHandler(channel_secret)
static_tmp_path = os.path.join(os.path.dirname(__file__), 'static', 'tmp')

# line_bot_api = settings.line_bot_api
# handler = settings.handler
# static_tmp_path = settings.static_tmp_path

def run():
    port = int(os.getenv("PORT", 5000))
    # # create tmp dir for download content
    make_static_tmp_dir()
    app.run(host="0.0.0.0", port=port)

# function for create tmp dir for download content
def make_static_tmp_dir():
    try:
        os.makedirs(static_tmp_path)
    except OSError as exc:
        if exc.errno == errno.EEXIST and os.path.isdir(static_tmp_path):
            pass
        else:
            raise

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
    gnavi = Gnavi(settings.gnavi_key, event)
    gnavi_data = gnavi.gnavi()
    shop_name = gnavi_data['name']
    shop_address = gnavi_data['address']
    destatitude = gnavi_data['Latitude']
    deestLongitude = gnavi_data['Longitude']
    shop_image = gnavi_data['shop_image1']
    destLatitude = str(destatitude)
    destLongitude = str(deestLongitude)
    route_url = 'http://maps.google.com/maps'\
                + '?saddr=' + srcLatitude + ',' + srcLongitude\
                + '&daddr=' + destLatitude + ',' + destLongitude\
                + '&dirflg=w'
    buttons_template = ButtonsTemplate(
        title=shop_name, text='ここからのルートを表示します', actions=[
            URITemplateAction(
                label='ルートを表示', uri=route_url),
        ])
    template_message = TemplateSendMessage(
        alt_text='Buttons', template=buttons_template)
    line_bot_api.reply_message(event.reply_token, template_message)
