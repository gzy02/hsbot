from .utility import connect_and_close_database, Classic_Mode_CardClassMap, cardClassMap, aliasesClassMap, JJCCardsSetPath, SYSTEM_ADMIN_QQ_NUMBER
from . import minion_query, cards_query, jjc_aomi_query, class_performance
from . import models
from .query import find_minion_by_body, find_card_by_text, find_card_by_name
from . import ask_json
from nonebot.adapters.onebot.v11 import Bot, MessageEvent, MessageSegment, Message
import json


@jjc_aomi_query.handle()
@connect_and_close_database
async def _jjc_aomi_query(bot: Bot, event: MessageEvent):
    """jjc奥秘+职业名"""
    try:
        with open(JJCCardsSetPath, "r", encoding="utf8") as fd:
            JJCCardsSet = json.loads(fd.read())["JJCCardsSet"]
    except Exception as e:
        jjc_aomi_query.finish(
            f"打开JJCCardsSet.json文件错误，请联系系统管理员[QQ:{SYSTEM_ADMIN_QQ_NUMBER}]\n错误如下：\n{repr(e)}")

    try:
        text = event.get_plaintext()  #获取纯文本 去除表情和图片
        text_list = text.split()

        if len(text_list) == 2:
            card_text = "奥秘："  # 注意这里应该有冒号
            zhiye = text_list[1]
            if text_list[1] in aliasesClassMap:
                zhiye = aliasesClassMap[text_list[1]]  # 转换成标准中文职业
            try:
                tep = find_card_by_text(card_text)
                message_str = f"现今环境中{zhiye}的奥秘有:\n"
                i = 0
                for j in tep:
                    if j.cardClass == cardClassMap[zhiye] and j.set in JJCCardsSet:
                        message_str += str(i + 1) + '. ' + j.name + '\n'
                        i += 1
                if event.message_type == "group":
                    message_str = f'[CQ:at,qq={event.get_user_id()}]' + message_str
                message_str += "如需浏览具体卡牌信息，可通过“查描述+卡牌名”指令查询"
                await jjc_aomi_query.send(message=Message(message_str.strip()))
            except Exception as e:
                await jjc_aomi_query.send(message=f"您的输入有误，请输入“jjc奥秘 xxx”，例如“jjc奥秘 法师”")
    except Exception as e:
        await jjc_aomi_query.finish(
            f'[jjc奥秘]程序错误，请联系系统管理员[QQ:{SYSTEM_ADMIN_QQ_NUMBER}]\n错误如下：\n{repr(e)}')


@cards_query.handle()
@connect_and_close_database
async def _cards_query(bot: Bot, event: MessageEvent):
    """查卡牌+卡牌名/描述"""
    try:
        text = event.get_plaintext()  #获取纯文本 去除表情和图片
        text_list = text.split()
        if len(text_list) == 2:
            try:  # 卡牌名字、描述
                card_text = text_list[1]
                tep = find_card_by_text(card_text)
                message_str = f"名称或描述中包含{card_text}的卡牌有:\n"
                for i, j in enumerate(tep):
                    message_str += str(i + 1) + '. ' + j.name + '\n'
                message_str += "如需浏览具体卡牌信息，可通过“查描述+卡牌名”指令查询"
                if event.message_type == "group":
                    message_str = f'[CQ:at,qq={event.get_user_id()}]' + message_str
                await cards_query.send(message=Message(message_str.strip()))
            except:
                await cards_query.send(message="您的输入有误，请输入“查卡牌 xxx”，例如“查卡牌 叫嚣的中士”")
    except Exception as e:
        await cards_query.finish(
            f'[查卡牌]程序错误，请联系系统管理员[QQ:{SYSTEM_ADMIN_QQ_NUMBER}]\n错误如下：\n{repr(e)}')


@minion_query.handle()
@connect_and_close_database
async def _minion_query(bot: Bot, event: MessageEvent):
    """查随从+身材"""
    try:
        text = event.get_plaintext()  #获取纯文本 去除表情和图片
        text_list = text.split()
        if len(text_list) == 2:
            if text_list[0] == "查随从":
                try:  # 根据身材查询
                    value_list = text_list[1].split('-')
                    if len(value_list) == 3:
                        minion_cost = value_list[0]
                        minion_attack = value_list[1]
                        minion_health = value_list[2]
                        message_str = find_minion_by_body(minion_cost, minion_attack, minion_health)
                        message_str += "如需浏览具体卡牌信息，可通过“查描述+卡牌名”指令查询"
                        if event.message_type == "group":
                            message_str = f'[CQ:at,qq={event.get_user_id()}]' + message_str
                        await minion_query.send(message=Message(message_str.strip()))
                    elif len(value_list) == 1:  # 类似"939" 不带 -
                        minion_cost = value_list[0][0]
                        minion_attack = value_list[0][1]
                        minion_health = value_list[0][2]
                        message_str = find_minion_by_body(minion_cost, minion_attack, minion_health)
                        message_str += "如需浏览具体卡牌信息，可通过“查描述+卡牌名”指令查询"
                        if event.message_type == "group":
                            message_str = f'[CQ:at,qq={event.get_user_id()}]' + message_str
                        await minion_query.send(message=Message(message_str.strip()))
                    else:
                        await minion_query.send(message="您的输入有误，请输入“查随从 x-x-x”，例如“查随从 9-3-9”")
                except:
                    await minion_query.send(message="您的输入有误，请输入“查随从 x-x-x”，例如“查随从 9-3-9”")
    except Exception as e:
        await minion_query.finish(
            f'[查随从]程序错误，请联系系统管理员[QQ:{SYSTEM_ADMIN_QQ_NUMBER}]\n错误如下：\n{repr(e)}')


def get_win_rate(gametype: int, res_json, cardClassMap) -> str:
    """查胜率+职业名 工具函数"""
    res_list = []
    for key, value in cardClassMap.items():
        for k in res_json['data'][value]:
            if k['game_type'] == gametype:
                res_list.append([key, k['win_rate']])
                break
    res_list.sort(reverse=True, key=lambda x: x[1])
    message_str = "模式下各职业胜率如下：\n"
    for i in res_list:
        message_str += i[0] + ': ' + str(i[1]) + '%\n'
    return message_str.strip()


@class_performance.handle()
async def _class_performance(bot: Bot, event: MessageEvent):
    """查胜率+职业名"""
    try:
        text = event.get_plaintext()  #获取纯文本 去除表情和图片
        text_list = text.split()
        if len(text_list) == 2:
            gametype = -1
            res_json = ask_json.get_performance_data()
            if res_json['status'] != 1:
                await class_performance.send(
                    message=f"hsbot与hsreplay的网络连接不佳，请联系系统管理员[QQ:{SYSTEM_ADMIN_QQ_NUMBER}]")
                #fp = open("performance_data.json", "r", encoding="utf8")
                #res_json = json.loads(fp.read())
            else:
                res_json = res_json['series']
                if text_list[1] == "标准":
                    gametype = 2
                    await class_performance.send(message="标准" +
                                                 get_win_rate(gametype, res_json, cardClassMap))
                elif text_list[1] == "狂野":
                    gametype = 30
                    await class_performance.send(message="狂野" +
                                                 get_win_rate(gametype, res_json, cardClassMap))
                elif text_list[1] == "经典":  # 没有恶魔猎手
                    gametype = 58
                    await class_performance.send(
                        message="经典" + get_win_rate(gametype, res_json, Classic_Mode_CardClassMap))
                elif text_list[1] == "竞技场" or text_list[1] == "jjc":
                    gametype = 3
                    await class_performance.send(message="竞技场" +
                                                 get_win_rate(gametype, res_json, cardClassMap))
                elif text_list[1] == "对决":
                    gametype = 55
                    await class_performance.send(message="对决" +
                                                 get_win_rate(gametype, res_json, cardClassMap))
                else:
                    await class_performance.send(message="您的输入有误，请输入“查胜率 xx”，例如“查胜率 jjc”")
        else:
            await class_performance.send(message="您的输入有误，请输入“查胜率 xx”，例如“查胜率 jjc”")
    except Exception as e:
        await class_performance.finish(
            f'[查胜率]程序错误，请联系系统管理员[QQ:{SYSTEM_ADMIN_QQ_NUMBER}]\n错误如下：\n{repr(e)}')
