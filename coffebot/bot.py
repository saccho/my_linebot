from __future__ import unicode_literals

import os
import sys
import urllib3

from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
    SourceUser, SourceGroup, SourceRoom,
    TemplateSendMessage, ConfirmTemplate, MessageTemplateAction,
    ButtonsTemplate, ImageCarouselTemplate, ImageCarouselColumn, URITemplateAction,
    CarouselTemplate, CarouselColumn, LocationMessage, LocationSendMessage,
)


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
