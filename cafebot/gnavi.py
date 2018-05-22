#!/usr/bin/env python
# -*- coding: utf-8 -*-
#*****************************************************************************************
# ぐるなびWebサービスのレストラン検索APIで緯度経度検索を実行しパースするプログラム
# 注意：ここでは緯度と経度の値は固定でいれています。
#       APIアクセスキーの値にはユーザ登録で取得したものを入れてください。
#*****************************************************************************************
import sys
import urllib3
import json
import settings

####
# 変数の型が文字列かどうかチェック
####
def is_str(data=None):
  if isinstance(data, str) or isinstance(data, unicode):
      return True
  else:
      return False

class Gnavi(object):
    def __init__(self):
        self.url = settings.gnavi_url

    def gnavi(self):
    # API実行
    try:
        result = urllib3.urlopen(self.url).read()
    except ValueError:
        return 'APIアクセスに失敗しました。'

    ####
    # 取得した結果を解析
    ####
    data = json.loads(result)

    # エラーの場合
    if 'error' in data:
        if 'message' in data:
            return '{0}'.format(data['message'])
        else:
            return 'データ取得に失敗しました。'

    # ヒット件数取得
    total_hit_count = None
    if 'total_hit_count' in data:
        total_hit_count = data['total_hit_count']

    # ヒット件数が0以下、または、ヒット件数がなかったら終了
    if total_hit_count is None or total_hit_count <= 0:
        return '指定した内容ではヒットしませんでした。'

    # レストランデータがなかったら終了
    if not 'rest' in data:
        return 'レストランデータが見つからなかったため終了します。'

    gnavi_data = {}
    # レストランデータ取得
    for rest in data['rest']:
        # 店舗名
        if 'name' in rest and is_str(rest['name']):
            name = u'{0}'.format(rest['name'])
            gnavi_data['name'] = name
        # 住所
        if 'address' in rest and is_str(rest['address']):
            address = u'{0}'.format(rest['address'])
            gnavi_data['address'] = address
        # 緯度
        if 'latitude' in rest and is_str(rest['latitude']):
            latitude = u'{0}'.format(rest['latitude'])
            gnavi_data['latitude'] = latitude
        # 経度
        if 'longitude' in rest and is_str(rest['longitude']):
            longitude = u'{0}'.format(rest['longitude'])
            gnavi_data['longitude'] = longitude
        # 店画像
        if 'shop_image1' in rest and is_str(rest['shop_image1']):
            shop_image1 = u'{0}'.format(rest['shop_image1'])
            gnavi_data['shop_image1'] = shop_image1
    return gnavi_data
