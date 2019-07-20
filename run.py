#!/usr/bin/env python
# -*- coding: utf-8 -*
from backend.app.models import vue_app, replace_str, read_csv
from flask import render_template, request, make_response
import json

app = vue_app()

station_master_list = read_csv('datasets/todofuken.txt')


@app.route('/', methods=["GET", "POST"])
def index():
    # js側でjson形式の文字列を取得する
    if type(request.json) is not dict:
        print(type(request.json))
        return make_response("")
    # 文章置換
    after_text_dict = replace_str(station_master_list, request.json)
    print('これは置換後のテキストです')
    print(after_text_dict)
    return after_text_dict


if __name__ == '__main__':
    app.run()
