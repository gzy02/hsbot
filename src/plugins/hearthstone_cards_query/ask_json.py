import requests

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36 Edg/100.0.1185.44'
}

def get_cards_json(json_url:str):
    """向api.hearthstonejson.com获取信息，存储在json_url"""
    url = 'https://api.hearthstonejson.com/v1/latest/zhCN/cards.collectible.json'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36 Edg/100.0.1185.44'
    }
    resp = requests.get(url, headers=headers)
    with open(json_url, "w", encoding="utf8") as fp:
        fp.write(resp.text)



def get_performance_data() -> dict:
    """
    :return: performance data
    """
    url = 'https://hsreplay.net/analytics/query/player_class_performance_summary/'

    res=dict()
    try:
        resp=requests.get(url,headers=headers)
        resp_json = resp.json()
        if resp.status_code == 200:
            res['status'] = 1
            res['series'] = resp_json['series']
        else:
            res['status'] = 0
    except:
        res['status'] = 0

    return res


def get_jjc_data() -> dict:
    """
    :return: jjc data
    """
    url = 'https://hsreplay.net/analytics/query/card_list_free/?GameType=ARENA&TimeRange=CURRENT_PATCH'

    res=dict()
    try:
        resp = requests.get(url, headers=headers)
        resp_json=resp.json()
        if resp.status_code==200:
            res['status']=1
            res['series']=resp_json['series']
        else:
            res['status']=0
    except:
        res['status']=0
        
    return res
        