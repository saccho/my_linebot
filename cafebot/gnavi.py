#!/usr/bin/env python3
# coding: utf-8

import sys
import urllib
import json

class Gnavi(object):
    def __init__(self, gnavi_key, event):
        self.url = "https://api.gnavi.co.jp/RestSearchAPI/20150630/?"
        latitude = str(event.message.latitude)
        longitude = str(event.message.longitude)
        # 範囲(range=1で300m以内)
        range = "1"
        query = [
            ("keyid", gnavi_key),
            ("format", "json"),
            ("latitude", latitude),
            ("longitude", longitude),
<<<<<<< HEAD
            ("range", range),
            ("category_l", "RSFST18000")
=======
            ("range", range)
>>>>>>> origin/master
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

        # レストランデータ取得
        for rest in data['rest']:
            # 店舗名
            if 'name' in rest:
                name = '{}'.format(rest['name'])
                self.gnavi_data['name'] = name
            # 住所
            if 'address' in rest:
                address = '{}'.format(rest['address'])
                self.gnavi_data['address'] = address
            # 緯度
            if 'latitude' in rest:
                latitude = '{}'.format(rest['latitude'])
                self.gnavi_data['latitude'] = latitude
            # 経度
            if 'longitude' in rest:
                longitude = '{}'.format(rest['longitude'])
                self.gnavi_data['longitude'] = longitude
        return self.gnavi_data
