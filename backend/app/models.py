#!/usr/bin/env python
# -*- coding: utf-8 -*
"""
モデル(関数、クラス、フィールド、メソッドなど)を定義する。
"""

from flask import Flask, jsonify, render_template, Blueprint
from flask_cors import CORS
import csv


def vue_app(app_name="VUE-FLASK"):
    """
    flask appの初期設定
    """
    app = Flask(
        app_name,
        static_folder="./dist/static",
        template_folder="./dist"
    )
    app.config.from_object('backend.app.settings.config.BaseConfig')
    CORS(app, resources={'/*': {"origins": "*"}})
    return app


def read_csv(station_master):
    # 駅マスタファイルを開く
    csv_file = open(station_master, "r", encoding="utf-8")
    # 読み込み
    f = csv.reader(csv_file, delimiter=",",
                   doublequote=True, lineterminator="\n")
    header = next(f)
    station_master_dict = {}
    station_master_list = []
    # rowはlist
    for row in f:
        # 辞書登録
        station_master_dict[header[0]] = row[0]
        station_master_dict[header[1]] = row[1]
        # 辞書をリストに追加
        station_master_list.append(station_master_dict)
        # 初期化
        station_master_dict = {}
    print(station_master_list)
    return station_master_list


def replace_str(station_master_list, before_text):
    """
    駅名置換関数
    送られてきたファイルの中身を「駅名」を駅名マスタの駅名に置換し、リストを返す
    """
    print('元の文章')
    print(before_text)
    # 変換後の文章を格納するdict
    after_text_dict = {}
    results_text = []
    if "「駅名」" in before_text['beforeText']:
        for city in station_master_list:
            print(city['pref_name'])
            after_text = before_text['beforeText'].replace(
                '「駅名」', city['pref_name'])
            print(after_text)
            # after_text_dict[city['pref_name']] = after_text
            after_text_dict['city_text'] = after_text
            print(after_text_dict)
            results_text.append(after_text_dict)
            after_text_dict = {}
        print(len(results_text))
        after_text_dict['after_text'] = results_text
        return after_text_dict


if __name__ == '__main__':
    # マスタダウンロード
    station_master_list = read_csv('datasets/todofuken.txt')
    replace_str(station_master_list,
                "「駅名」の牛肉専門家が200以上のブランド牛の中から口コミや消費量、有名店で扱われている数などを総合して、弊社オリジナルで算出したブランド牛・牛肉通販サイトのおすすめランキングを紹介します")
