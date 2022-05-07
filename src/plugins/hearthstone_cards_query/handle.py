
from . import minion_query, cards_query,jjc_aomi_query,jjc_choose,reset_database
from nonebot.adapters.onebot.v11 import Bot, MessageEvent, MessageSegment
from nonebot.rule import to_me

from . import models
from .query import find_minion_by_body, find_card_by_text
from . import read_json

import requests
def get_json(json_url):
    url = 'https://api.hearthstonejson.com/v1/latest/zhCN/cards.collectible.json'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36 Edg/100.0.1185.44'
    }
    resp=requests.get(url, headers=headers)
    with open(json_url,"w",encoding="utf8") as fp:
        fp.write(resp.text)

@reset_database.handle()
async def _reset_database(event: MessageEvent):
    #连接数据库
    if models.database.is_closed():
        models.database.connect()

    await reset_database.send(message="开始重置...")

    if models.MINIONCards.table_exists:
        models.MINIONCards.drop_table()
    if models.SPELLCards.table_exists:
        models.SPELLCards.drop_table()
    if models.HEROCards.table_exists:
        models.HEROCards.drop_table()
    if models.WEAPONCards.table_exists:
        models.WEAPONCards.drop_table()
    if models.Cards.table_exists:
        models.Cards.drop_table()

    models.Cards.create_table()
    models.MINIONCards.create_table()
    models.SPELLCards.create_table()
    models.WEAPONCards.create_table()
    models.HEROCards.create_table()

    json_url="cards.collectible.json"
    get_json(json_url)
    read_json.init_database_from_json(json_url)
    await reset_database.send(message="重置完成")

JJCCardsSet = ['CORE', 'LOE', 'OG', 'TGT', 'STORMWIND', 'THE_SUNKEN_CITY', 'ALTERAC_VALLEY']
"""
当前竞技场轮换卡池：
核心系列
探险者协会
上古之神的低语
冠军的试炼
暴风城下的集结
奥特兰克的决裂
探寻沉没之城
"""
aliasesClassMap={"法":"法师","猎":"猎人","牧":"牧师","战":"战士","贼":"潜行者","德":"德鲁伊","萨":"萨满","术":"术士","骑士":"圣骑士","骑":"圣骑士","瞎":"恶魔猎手"}
cardClassMap={"法师":"MAGE","猎人":"HUNTER","牧师":"PRIEST","术士":"WARLOCK", "潜行者":"ROGUE", "德鲁伊":"DRUID", "萨满":"SHAMAN","战士": "WARRIOR", "圣骑士":"PALADIN", "恶魔猎手":"DEMONHUNTER"}
@jjc_aomi_query.handle()
async def _jjc_aomi_query(bot: Bot,event: MessageEvent):
    #连接数据库
    if models.database.is_closed():
        models.database.connect()


    for i in event.get_message():  #获取该事件中每条消息
        print(i.data)
        if i.type == "text":  #文本
            text_list = i.data['text'].split()
            print(text_list)
            if len(text_list) == 2:
                card_text="奥秘："#注意这里应该有冒号
                zhiye=text_list[1]
                if text_list[1] in aliasesClassMap:
                    zhiye=aliasesClassMap[text_list[1]]#转换成标准中文职业
                try:
                    tep = find_card_by_text(card_text)
                    message_str = f"现今环境中{zhiye}的奥秘有:\n"

                    i=0
                    for j in tep:
                        if j.cardClass == cardClassMap[zhiye] and j.set in JJCCardsSet:
                            message_str += str(i + 1) + '. ' + j.name + '\n'
                            i+=1
                    await jjc_aomi_query.send(message=message_str)
                except:  #
                    await jjc_aomi_query.send(message="您的输入有误，请输入“jjc奥秘 xxx”，例如“jjc奥秘 法师”")



    #请求结束，关数据库
    if not models.database.is_closed():
        models.database.close()


@cards_query.handle()
async def _cards_query(bot: Bot, event: MessageEvent):
    #连接数据库
    if models.database.is_closed():
        models.database.connect()

    for i in event.get_message():  #获取该事件中每条消息
        print(i.data)
        if i.type == "text":  #文本
            text_list = i.data['text'].split()
            print(text_list)
            if len(text_list) == 2:
                try:  #卡牌名字、描述
                    card_text = text_list[1]
                    tep = find_card_by_text(card_text)
                    message_str = f"名称或描述中包含{card_text}的卡牌有:\n"
                    for i, j in enumerate(tep):
                        message_str += str(i + 1) + '. ' + j.name + '\n'
                    await cards_query.send(message=message_str)
                except:  #
                    await cards_query.send(message="您的输入有误，请输入“查卡牌 xxx”，例如“查卡牌 叫嚣的中士”")

    #请求结束，关数据库
    if not models.database.is_closed():
        models.database.close()


@minion_query.handle()
async def _minion_query(bot: Bot, event: MessageEvent):
    #连接数据库
    if models.database.is_closed():
        models.database.connect()

    for i in event.get_message():  #获取该事件中每条消息
        print(i.data)
        if i.type == "text":  #文本
            text_list = i.data['text'].split()
            if len(text_list) == 2:
                if text_list[0] == "查随从":
                    try:  #根据身材查询
                        value_list = text_list[1].split('-')
                        if len(value_list) == 3:
                            minion_cost = value_list[0]
                            minion_attack = value_list[1]
                            minion_health = value_list[2]
                            message_str = find_minion_by_body(minion_cost, minion_attack, minion_health)
                            await minion_query.send(message=message_str)
                        elif len(value_list) == 1:  #类似"939" 不带 -
                            minion_cost = value_list[0][0]
                            minion_attack = value_list[0][1]
                            minion_health = value_list[0][2]
                            message_str = find_minion_by_body(minion_cost, minion_attack, minion_health)
                            await minion_query.send(message=message_str)
                        else:
                            await minion_query.send(message="您的输入有误，请输入“查随从 x-x-x”，例如“查随从 9-3-9”")
                    except:
                        await minion_query.send(message="您的输入有误，请输入“查随从 x-x-x”，例如“查随从 9-3-9”")

    #请求结束，关数据库
    if not models.database.is_closed():
        models.database.close()


import json
@jjc_choose.handle()
async def _jjc_choose(bot:Bot,event:MessageEvent):
    for i in event.get_message():
        if i.type=='text':
            text_list=i.data['text'].split()
            print(text_list)
            if len(text_list)>2:
                #别名，不指定默认全职业
                aliasesClassMap={"法":"法师","猎":"猎人","牧":"牧师","战":"战士","贼":"潜行者","德":"德鲁伊","萨":"萨满祭司","萨满":"萨满祭司","术":"术士","骑士":"圣骑士","骑":"圣骑士","瞎":"恶魔猎手"}
                cardClassMap={"全职业":"ALL","法师":"MAGE","猎人":"HUNTER","牧师":"PRIEST","术士":"WARLOCK", "潜行者":"ROGUE", "德鲁伊":"DRUID", "萨满祭司":"SHAMAN","战士": "WARRIOR", "圣骑士":"PALADIN", "恶魔猎手":"DEMONHUNTER"}
                zhiye=text_list[1]
                cur_class="error"
                if zhiye in aliasesClassMap:
                    zhiye=aliasesClassMap[zhiye]
                if zhiye in cardClassMap:
                    cur_class=cardClassMap[zhiye]
                if cur_class=="error":
                    await jjc_choose.send(message="您的输入有误，请输入“jjc选牌 <职业> <卡牌名>”，例如“jjc选牌 德 奇迹生长”")
                else:
                    query_dir={}
                    for i in range(len(text_list)-2):
                        print(text_list[i+2])
                        tep=find_card_by_text(text_list[i+2])
                        for j in tep:
                            if j.set in JJCCardsSet:#当前jjc套牌池
                                query_dir[j.dbfid]=j.name

                    #res_json=(await ask_json.get_jjc_data())
                    #if res_json['status']!=1:
                    #    await jjc_choose.send(message="网络连接不佳，请稍后再试")
                    fp=open("jjc_winrate.json","r",encoding="utf8")
                    res_json=json.loads(fp.read())
                    res_json=res_json['series']
                    message_str="以上卡牌的jjc数据如下：\n"
                    cnt=1
                    max_winrate=0
                    recommand_card=""
                    for item in res_json['data'][cur_class]:
                        if item['dbf_id'] in query_dir:
                            if item['included_winrate']>max_winrate:
                                max_winrate=item['included_winrate']
                                recommand_card=query_dir[item['dbf_id']]
                            message_str+=str(cnt)+'. '+query_dir[item['dbf_id']]+'\n'
                            message_str+='包含此牌的卡组胜率:'+str(item['included_winrate'])+'\n'
                            message_str+='打出胜率:'+str(item['winrate_when_played'])+'\n'
                            message_str+='套牌中出现概率:'+str(item['included_popularity'])+'\n'
                            message_str+='套牌中平均张数:'+str(item['included_count'])+'\n'
                            message_str+='打出次数'+str(item['times_played'])+'\n'
                            cnt+=1
                    message_str+="\n推荐选取："+recommand_card
                    if recommand_card=="":
                        await jjc_choose.send(message="未在当前jjc卡池中找到您的输入卡牌，请重新输入")
                    else:
                        await jjc_choose.send(message=message_str)

            else:
                await jjc_choose.send(message="您的输入有误，请输入“jjc选牌 <职业> <卡牌名>”，例如“jjc选牌 德 奇迹生长”")

