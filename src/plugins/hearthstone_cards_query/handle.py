from .utility import connect_and_close_database,cardClassMap,aliasesClassMap,JJCCardsSetPath,SYSTEM_ADMIN_QQ_NUMBER
from . import minion_query, cards_query, jjc_aomi_query, jjc_choose,class_performance,build_cards,pic_query
from . import models
from .query import find_minion_by_body, find_card_by_text,find_card_by_name
from . import ask_json
from nonebot.adapters.onebot.v11 import Bot, MessageEvent, MessageSegment,Message
import json

@jjc_aomi_query.handle()
@connect_and_close_database
async def _jjc_aomi_query(bot: Bot, event: MessageEvent):
    """jjc奥秘+职业名"""
    try:
        with open(JJCCardsSetPath, "r", encoding="utf8") as fd:
            JJCCardsSet = json.loads(fd.read())["JJCCardsSet"]
    except Exception as e:
        jjc_aomi_query.finish(f"打开JJCCardsSet.json文件错误，请联系系统管理员[QQ:{SYSTEM_ADMIN_QQ_NUMBER}]\n错误如下：\n{repr(e)}")

    try:
        text=event.get_plaintext()#获取纯文本 去除表情和图片
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
                if event.message_type=="group":
                    message_str=f'[CQ:at,qq={event.get_user_id()}]'+message_str
                await jjc_aomi_query.send(message=Message(message_str.strip()))
            except Exception as e: 
                await jjc_aomi_query.send(message=f"您的输入有误，请输入“jjc奥秘 xxx”，例如“jjc奥秘 法师”")
    except Exception as e:
        await jjc_aomi_query.finish(f'[jjc奥秘]程序错误，请联系系统管理员[QQ:{SYSTEM_ADMIN_QQ_NUMBER}]\n错误如下：\n{repr(e)}')

@cards_query.handle()
@connect_and_close_database
async def _cards_query(bot: Bot, event: MessageEvent):
    """查卡牌+卡牌名/描述"""
    try:
        text=event.get_plaintext()#获取纯文本 去除表情和图片
        text_list = text.split()
        if len(text_list) == 2:
            try:  # 卡牌名字、描述
                card_text = text_list[1]
                tep = find_card_by_text(card_text)
                message_str = f"名称或描述中包含{card_text}的卡牌有:\n"
                for i, j in enumerate(tep):
                    message_str += str(i + 1) + '. ' + j.name + '\n'
                message_str+="如需浏览具体卡牌信息，可通过“查描述+卡牌名”指令查询"
                if event.message_type=="group":
                    message_str=f'[CQ:at,qq={event.get_user_id()}]'+message_str
                await cards_query.send(message=Message(message_str.strip()))
            except: 
                await cards_query.send(message="您的输入有误，请输入“查卡牌 xxx”，例如“查卡牌 叫嚣的中士”")
    except Exception as e:
        await cards_query.finish(f'[查卡牌]程序错误，请联系系统管理员[QQ:{SYSTEM_ADMIN_QQ_NUMBER}]\n错误如下：\n{repr(e)}')


@minion_query.handle()
@connect_and_close_database
async def _minion_query(bot: Bot, event: MessageEvent):
    """查随从+身材"""
    try:
        text=event.get_plaintext()#获取纯文本 去除表情和图片
        text_list = text.split()
        if len(text_list) == 2:
            if text_list[0] == "查随从":
                try:  # 根据身材查询
                    value_list = text_list[1].split('-')
                    if len(value_list) == 3:
                        minion_cost = value_list[0]
                        minion_attack = value_list[1]
                        minion_health = value_list[2]
                        message_str = find_minion_by_body(
                            minion_cost, minion_attack, minion_health)
                        message_str+="如需浏览具体卡牌信息，可通过“查描述+卡牌名”指令查询"
                        if event.message_type=="group":
                            message_str=f'[CQ:at,qq={event.get_user_id()}]'+message_str
                        await minion_query.send(message=Message(message_str.strip()))
                    elif len(value_list) == 1:  # 类似"939" 不带 -
                        minion_cost = value_list[0][0]
                        minion_attack = value_list[0][1]
                        minion_health = value_list[0][2]
                        message_str = find_minion_by_body(
                            minion_cost, minion_attack, minion_health)
                        message_str+="如需浏览具体卡牌信息，可通过“查描述+卡牌名”指令查询"
                        if event.message_type=="group":
                            message_str=f'[CQ:at,qq={event.get_user_id()}]'+message_str
                        await minion_query.send(message=Message(message_str.strip()))
                    else:
                        await minion_query.send(message="您的输入有误，请输入“查随从 x-x-x”，例如“查随从 9-3-9”")
                except:
                    await minion_query.send(message="您的输入有误，请输入“查随从 x-x-x”，例如“查随从 9-3-9”")
    except Exception as e:
        await minion_query.finish(f'[查随从]程序错误，请联系系统管理员[QQ:{SYSTEM_ADMIN_QQ_NUMBER}]\n错误如下：\n{repr(e)}')

@jjc_choose.handle()
@connect_and_close_database
async def _jjc_choose(bot: Bot, event: MessageEvent):
    "jjc选牌+卡牌名列表"
    try:
        with open(JJCCardsSetPath, "r", encoding="utf8") as fd:
            JJCCardsSet = json.loads(fd.read())["JJCCardsSet"]
    except Exception as e:
        jjc_choose.finish(f"程序错误，请联系系统管理员[QQ:{SYSTEM_ADMIN_QQ_NUMBER}]\n错误如下：\n{repr(e)}")
    try:
        text=event.get_plaintext()#获取纯文本 去除表情和图片
        text_list = text.split()
        if len(text_list) > 2:
            # 别名，不指定默认全职业
            cardClassMap = {"全职业": "ALL", "法师": "MAGE", "猎人": "HUNTER", "牧师": "PRIEST", "术士": "WARLOCK", "潜行者": "ROGUE",
                            "德鲁伊": "DRUID", "萨满祭司": "SHAMAN", "战士": "WARRIOR", "圣骑士": "PALADIN", "恶魔猎手": "DEMONHUNTER"}
            zhiye = text_list[1]
            cur_class = "error"
            if zhiye in aliasesClassMap:
                zhiye = aliasesClassMap[zhiye]
            if zhiye in cardClassMap:
                cur_class = cardClassMap[zhiye]
            if cur_class == "error":
                await jjc_choose.send(message="您的输入有误，请输入“jjc选牌 <职业> <卡牌名>”，例如“jjc选牌 德 奇迹生长”")
            else:
                query_dir = {}
                for i in range(len(text_list) - 2):
                    
                    need=[models.Cards.name,models.Cards.cardClass, models.Cards.dbfid, models.Cards.id, models.Cards.text,models.Cards.set]
                    found=False
                    
                    teps=models.Cards.select(*need).where(models.Cards.name==text_list[i + 2])
                    for tep in teps:
                        if tep.set in JJCCardsSet:
                            query_dir[tep.dbfid]=tep.name
                            found=True
                            break
                    if found==False:
                        tep = find_card_by_name(text_list[i + 2])
                        for j in tep:
                            if j.set in JJCCardsSet:  # 当前jjc套牌池
                                query_dir[j.dbfid] = j.name

                res_json=ask_json.get_jjc_data()
                if res_json['status']!=1:
                    await jjc_choose.send(message=f"hsbot与hsreplay的网络连接不佳，请联系系统管理员[QQ:{SYSTEM_ADMIN_QQ_NUMBER}]")
                    #或者读取本地
                    #fp = open("jjc_winrate.json", "r", encoding="utf8")
                    #res_json = json.loads(fp.read())
                else:
                    res_json = res_json['series']
                    message_str = "以上卡牌的jjc数据如下：\n"
                    cnt = 1
                    max_winrate = 0
                    recommand_card = ""
                    
                    for item in res_json['data'][cur_class]:
                        if item['dbf_id'] in query_dir:
                            if item['included_winrate'] > max_winrate:
                                max_winrate = item['included_winrate']
                                recommand_card = query_dir[item['dbf_id']]
                            message_str += str(cnt) + '. ' + \
                                query_dir[item['dbf_id']] + '\n'
                            message_str += '包含此牌的卡组胜率:' + \
                                str(item['included_winrate']) + '\n'
                            message_str += '打出胜率:' + \
                                str(item['winrate_when_played']) + '\n'
                            message_str += '套牌中出现概率:' + \
                                str(item['included_popularity']) + '\n'
                            message_str += '套牌中平均张数:' + \
                                str(item['included_count']) + '\n'
                            message_str += '打出次数' + \
                                str(item['times_played']) + '\n'
                            cnt += 1
                    message_str += "\n推荐选取：" + recommand_card
                    if recommand_card == "":
                        await jjc_choose.send(message="未在当前jjc卡池中找到您的输入卡牌，请重新输入")
                    else:
                        if event.message_type=="group":
                            message_str=f'[CQ:at,qq={event.get_user_id()}]'+message_str
                        await jjc_choose.send(message=Message(message_str.strip()))
        else:
            await jjc_choose.send(message="您的输入有误，请输入“jjc选牌 <职业> <卡牌名>”，例如“jjc选牌 德 奇迹生长”")
    except Exception as e:
        await jjc_choose.finish(f'[jjc选牌]程序错误，请联系系统管理员[QQ:{SYSTEM_ADMIN_QQ_NUMBER}]\n错误如下：\n{repr(e)}')


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
        text=event.get_plaintext()#获取纯文本 去除表情和图片
        text_list = text.split()
        if len(text_list) == 2:
            gametype = -1
            cardClassMap = {"法师": "MAGE", "猎人": "HUNTER", "牧师": "PRIEST", "术士": "WARLOCK", "潜行者": "ROGUE",
                            "德鲁伊": "DRUID", "萨满": "SHAMAN", "战士": "WARRIOR", "圣骑士": "PALADIN", "恶魔猎手": "DEMONHUNTER"}

            res_json = ask_json.get_performance_data()
            if res_json['status'] != 1:
                await class_performance.send(message=f"hsbot与hsreplay的网络连接不佳，请联系系统管理员[QQ:{SYSTEM_ADMIN_QQ_NUMBER}]")
                #fp = open("performance_data.json", "r", encoding="utf8")
                #res_json = json.loads(fp.read())
            else:
                res_json = res_json['series']
                if text_list[1] == "标准":
                    gametype = 2
                    await class_performance.send(message="标准" + get_win_rate(gametype, res_json, cardClassMap))
                elif text_list[1] == "狂野":
                    gametype = 30
                    await class_performance.send(message="狂野" + get_win_rate(gametype, res_json, cardClassMap))
                elif text_list[1] == "经典":  # 没有恶魔猎手
                    gametype = 58
                    cardClassMap = {"法师": "MAGE", "猎人": "HUNTER", "牧师": "PRIEST", "术士": "WARLOCK",
                                    "潜行者": "ROGUE", "德鲁伊": "DRUID", "萨满": "SHAMAN", "战士": "WARRIOR", "圣骑士": "PALADIN"}
                    await class_performance.send(message="经典" + get_win_rate(gametype, res_json, cardClassMap))
                elif text_list[1] == "竞技场" or text_list[1] == "jjc":
                    gametype = 3
                    await class_performance.send(message="竞技场" + get_win_rate(gametype, res_json, cardClassMap))
                elif text_list[1] == "对决":
                    gametype = 55
                    await class_performance.send(message="对决" + get_win_rate(gametype, res_json, cardClassMap))
                else:
                    await class_performance.send(message="您的输入有误，请输入“查胜率 xx”，例如“查胜率 jjc”")
        else:
            await class_performance.send(message="您的输入有误，请输入“查胜率 xx”，例如“查胜率 jjc”")
    except Exception as e:
        await class_performance.finish(f'[查胜率]程序错误，请联系系统管理员[QQ:{SYSTEM_ADMIN_QQ_NUMBER}]\n错误如下：\n{repr(e)}')





import re
from typing import Tuple
import base64
from urllib import parse
import requests
from PIL import Image
from io import BytesIO

def gethash(text: str) -> Tuple[bool, str]:
    """获取卡组图片的工具函数"""
    result = re.search('var hash = "(?P<hash>.*?)";', text)
    if result:
        return True, result.groupdict().get("hash")
    else:
        return False, "Not Found"


@build_cards.handle()
async def _build_cards(bot:Bot,event:MessageEvent):
    """无需指令主动触发，自动判断收到信息中是否含有炉石代码，详见https://zhuanlan.zhihu.com/p/142113610"""
    #获取卡组图片，可以先解析然后用PIL库拼接图片。不过对PIL库不是很熟，这里先调fbigame的库了
    try:
        text=event.get_plaintext()#获取纯文本 去除表情和图片
        deck_text = ""
        pattern="AAE[BCD]A"
        result=re.search(pattern,text)
        deck_code=""
        
        for l in range(result.regs[-1][0],len(text)):
            if text[l]!='\n':
                deck_code+=text[l]

        deck_code = parse.quote(deck_code) #注意+转%2B这种情况
        url = f"https://hs.fbigame.com/decks.php?deck_code={deck_code}"
        req = requests.get(url=url)
        if req.status_code==200:
            if "卡组代码错误" not in req.text:
                """这里不考虑卡组代码错误时的交互 认为是用户误触发"""
                hash = gethash(req.text)
                if hash[0] == True:
                    hash = hash[1]
                    #获取图片
                    url = f"https://hs.fbigame.com/ajax.php?mod=general_deck_image&deck_code={deck_code}&deck_text={deck_text}&hash={hash}"
                    req = requests.get(url=url)
                    img_text = eval(req.text)['img']
                    img = base64.urlsafe_b64decode(img_text)
                    PIL_img = Image.open(BytesIO(img))
                    print(PIL_img.size)
                    cropped = PIL_img.crop((0, 0, PIL_img.size[0],
                                            PIL_img.size[1] - 70))  # 裁剪图片
                    img_byte=BytesIO()
                    cropped.save(img_byte,format='PNG')
                    binary_str2=img_byte.getvalue()
                    await build_cards.send(message=MessageSegment.image(binary_str2))
                else:
                    await build_cards.send(message=f"hsbot未获取hs.fbigame.com对应hash凭证，请联系系统管理员[QQ:{SYSTEM_ADMIN_QQ_NUMBER}]")
        else:
            await build_cards.send(message=f"hsbot与hs.fbigame.com的网络连接不佳，请联系系统管理员[QQ:{SYSTEM_ADMIN_QQ_NUMBER}]")
    except Exception as e:
        await build_cards.finish(f'[卡组代码解析]程序错误，请联系系统管理员[QQ:{SYSTEM_ADMIN_QQ_NUMBER}]\n错误如下：\n{repr(e)}')



@pic_query.handle()
@connect_and_close_database
async def _pic_query(bot:Bot,event:MessageEvent):
    try:
        text=event.get_plaintext()#获取纯文本 去除表情和图片
        text_list = text.split()
        if len(text_list) > 1:
            for i in range(len(text_list) - 1):
                try:
                    tep=models.Cards.get(models.Cards.name==text_list[i + 1])
                    url=f"https://art.hearthstonejson.com/v1/render/latest/zhCN/256x/{tep.id}.png"
                    resp=requests.get(url)
                    if resp.status_code==200:
                        await pic_query.send(message=MessageSegment.image(resp._content))
                    else:
                        await build_cards.send(message=f"hsbot与art.hearthstonejson.com的网络连接不佳，请联系系统管理员[QQ:{SYSTEM_ADMIN_QQ_NUMBER}]")
                except:
                    tep = find_card_by_name(text_list[i + 1])
                    if tep.count()<=0:
                        await jjc_choose.send(message="您的输入有误，请输入“查卡图 <卡牌名>”，例如“查卡图 银背族长”")

                    for j in tep:
                        url=f"https://art.hearthstonejson.com/v1/render/latest/zhCN/256x/{j.id}.png"
                        resp=requests.get(url)
                        await pic_query.send(message=f"检测到输入卡牌名并非完整全称，仅显示符合名称包含{text_list[i+1]}的其中一张"+MessageSegment.image(resp._content))
                        break
        else:
            await jjc_choose.send(message="您的输入有误，请输入“查卡图 <卡牌名>”，例如“查卡图 银背族长”")
    except Exception as e:
        await build_cards.finish(f'[卡组代码解析]程序错误，请联系系统管理员[QQ:{SYSTEM_ADMIN_QQ_NUMBER}]\n错误如下：\n{repr(e)}')
