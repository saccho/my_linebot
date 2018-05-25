#!/usr/bin/env python
# -*- coding: utf-8 -*-
#*****************************************************************************************
# ぐるなびWebサービスのレストラン検索APIで緯度経度検索を実行しパースするプログラム
# 注意：ここでは緯度と経度の値は固定でいれています。
#       APIアクセスキーの値にはユーザ登録で取得したものを入れてください。
#*****************************************************************************************
import sys
import urllib
import json
# from cafebot import settings

####
# 変数の型が文字列かどうかチェック
####
def is_str(data=None):
  if isinstance(data, str) or isinstance(data, unicode):
      return True
  else:
      return False

class Gnavi(object):
    def __init__(self, gnavi_key, event):
        # エンドポイントURL
        self.url = "https://api.gnavi.co.jp/RestSearchAPI/20150630/?"
        # 緯度・経度、範囲を変数に入れる
        # 範囲はrange=1で300m以内を指定している。
        # 緯度
        latitude = str(event.message.latitude)
        # # 経度
        longitude = str(event.message.longitude)
        # 範囲
        range = "1"
        # URLに続けて入れるパラメータを組立
        query = [
            ("keyid", gnavi_key),
            ("format", "json"),
            ("latitude", latitude),
            ("longitude", longitude),
            ("range", range)
        ]
        # URL生成
        self.url += '{}'.format(urllib.parse.urlencode(query))
        self.total_hit_count = None
        self.gnavi_data = {}
        self.gnavi_data['error_message'] = None

    def gnavi(self):
        # API実行
        try:
            result = urllib.request.urlopen(self.url).read()
        except ValueError:
            self.gnavi_data['error_message'] = 'APIアクセスに失敗しました。'
        ####
        # 取得した結果を解析
        ####
        data = json.loads(result)

        # エラーの場合
        if 'error' in data:
            if 'message' in data:
                self.gnavi_data['error_message'] = '{}'.format(data['message'])
            else:
                self.gnavi_data['error_message'] = 'データ取得に失敗しました。'

        # ヒット件数取得
        if 'total_hit_count' in data:
            self.total_hit_count = data['total_hit_count']

        # ヒット件数が0以下、または、ヒット件数がなし
        if (self.total_hit_count == None) or (self.total_hit_count == 0):
            self.gnavi_data['error_message'] = '指定した内容ではヒットしませんでした。'

        # レストランデータがなし
        if not 'rest' in data:
            self.gnavi_data['error_message'] = 'レストランデータが見つかりませんでした。'

        # エラーの場合終了
        if not self.gnavi_data['error_message'] == None:
            return self.gnavi_data
        else:
            pass

        # レストランデータ取得
        for rest in data['rest']:
            # 店舗名
            if 'name' in rest and is_str(rest['name']):
                name = '{}'.format(rest['name'])
                self.gnavi_data['name'] = name
            # 住所
            if 'address' in rest and is_str(rest['address']):
                address = '{}'.format(rest['address'])
                self.gnavi_data['address'] = address
            # 緯度
            if 'latitude' in rest and is_str(rest['latitude']):
                latitude = '{}'.format(rest['latitude'])
                self.gnavi_data['latitude'] = latitude
            # 経度
            if 'longitude' in rest and is_str(rest['longitude']):
                longitude = '{}'.format(rest['longitude'])
                self.gnavi_data['longitude'] = longitude
            # # 店画像
            # if 'shop_image1' in rest and is_str(rest['shop_image1']):
            #     shop_image1 = '{}'.format(rest['shop_image1'])
            #     self.gnavi_data['shop_image1'] = shop_image1
        return self.gnavi_data
