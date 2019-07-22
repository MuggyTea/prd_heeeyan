#!/usr/bin/env python
# -*- coding: utf-8 -*
"""
モデル(関数、クラス、フィールド、メソッドなど)を定義する。
"""

from flask import Flask, jsonify, render_template, Blueprint
from flask_cors import CORS
import csv
from wordpress_xmlrpc import Client, WordpressPost
from wordpress_xmlrpc.methods.posts import GetPosts, NewPost
from wordpress_xmlrpc.methods.users import GetsUserInfo
import os
import glob
import ssl
from backend.app.settings.constants import URL, ID, PASS


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


def replace_str(station_master_list, article):
    """
    駅名置換関数
    送られてきたファイルの中身を「駅名」を駅名マスタの駅名に置換し、リストを返す
    """
    print('元の文章')
    print(article)
    # 変換後の文章を格納するdict
    after_text_dict = {}
    after_text_tmp = {}
    results_text = []
    if "「駅名」" not in article['beforeText']:
        article['after_city_text'] = article['beforeText']
        after_text_dict['after_text'] = article
        return after_text_dict
    else:
        for city in station_master_list:
            print(city['pref_name'])
            # 県ごとの記事を生成
            after_text = article['beforeText'].replace(
                '「駅名」', city['pref_name'])
            print('after_text: {}'.format(after_text))
            # after_text_dict[city['pref_name']] = after_text
            after_text_tmp['after_city_text'] = after_text
            after_text_tmp['title'] = article['title']
            after_text_tmp['category'] = article['category']
            # print(after_text_tmp)
            print('tmpファイル')
            print(article)
            # print(results_text)
            # after_text_tmp = article
            # 県ごとにリストに格納
            results_text.append(after_text_tmp)
            # results_text = results_text
            after_text_tmp = {}
        print(len(results_text))
        print(results_text)
        after_text_dict['after_text'] = results_text
        return after_text_dict


def send_wordpress(after_text_dict):
    """
    生成した記事を一括でwordpressブログに投稿するスクリプト
    """
    ssl._create_default_https_context = ssl._create_unverified_context
    try:
        wp = Client(URL, ID, Pass)
        for after_text in after_text_dict:
            print(after_text)
            # 投稿の準備
            post = WordpressPost()
            # タイトル
            post.title = after_text['title']
            # コンテンツ
            post.content = after_text['after_city_text']
            # 下書きに反映
            post.status = 'draft'
            # カテゴリ
            post.terms_names = {
                'category': [after_text['category']]
            }
            wp.call(NewPost(post))
    except Exception as e:
        print(e)


if __name__ == '__main__':
    # マスタダウンロード
    station_master_list = read_csv('datasets/todofuken.txt')
    article = {
        "title": "タイトル",
        "category": "カテゴリ",
        "beforeText": "「駅名」の牛肉専門家が200以上のブランド牛の中から口コミや消費量、有名店で扱われている数などを総合して、弊社オリジナルで算出したブランド牛・牛肉通販サイトのおすすめランキングを紹介します"
    }
    replace_str(station_master_list, article)
