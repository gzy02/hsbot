from . import minion_query, cards_query,jjc_aomi_query
from nonebot.adapters.onebot.v11 import Bot, MessageEvent, MessageSegment
from nonebot.rule import to_me

from . import models
from .query import find_minion_by_body, find_card_by_text

JJCCardsSet = ['CORE', 'LOE', 'OG', 'TGT', 'STORMWIND', 'VSC', 'ALTERAC_VALLEY']
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
                    print(type(tep))
                    message_str = f"名称或描述中包含{card_text}的卡牌有:\n"
                    for i, j in enumerate(tep):
                        message_str += str(i + 1) + '. ' + j.name + '\n'
                    await cards_query.send(message=message_str)
                except:  #
                    await cards_query.send(message="您的输入有误，请输入“查卡牌 xxx”，例如“查随从 叫嚣的中士”")

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