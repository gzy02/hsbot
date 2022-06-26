# -*- coding: utf8 -*-
#linux版，跟hsreplay有关的请求不用request而是用curl，因为前者返回的结果全是乱码

import requests


def get_cards_json(json_url: str):
    """最新卡牌json_url"""
    url = 'https://api.hearthstonejson.com/v1/latest/zhCN/cards.collectible.json'
    resp = requests.get(url)
    with open(json_url, "w", encoding="utf8") as fp:
        fp.write(resp.text)


def get_performance_data() -> dict:
    """
    :return: performance data
    """
    url = 'https://hsreplay.net/analytics/query/player_class_performance_summary/'
    res = dict()
    try:
        resp = os.popen("curl " + url).read()
        #with open("test.json", "w") as fp:
        #    print(type(resp))
        #    fp.write(resp)
        resp_json = json.loads(resp)
        res['status'] = 1
        res['series'] = resp_json['series']

    except Exception as e:
        print(repr(e))
        res['status'] = 0

    return res


import json
import os


def get_jjc_data() -> dict:
    """
    :return: jjc data
    """
    url = 'https://hsreplay.net/analytics/query/card_list_free/?GameType=ARENA&TimeRange=CURRENT_PATCH'

    res = dict()
    try:
        resp = os.popen("curl " + url).read()
        #with open("test.json", "w") as fp:
        #    print(type(resp))
        #    fp.write(resp)
        resp_json = json.loads(resp)
        res['status'] = 1
        res['series'] = resp_json['series']

    except Exception as e:
        print(repr(e))
        res['status'] = 0

    return res


if __name__ == "__main__":
    pass
    #get_jjc_data()
    #get_performance_data()
    #get_cards_json("test.json")
