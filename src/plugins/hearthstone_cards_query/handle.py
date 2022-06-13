from .utility import connect_and_close_database,cardClassMap,aliasesClassMap,JJCCardsSetPath,SYSTEM_ADMIN_QQ_NUMBER
from . import minion_query, cards_query, jjc_aomi_query, jjc_choose,class_performance,build_cards,pic_query
from . import models
from .query import find_minion_by_body, find_card_by_text,find_card_by_name
from . import ask_json
from nonebot.adapters.onebot.v11 import Bot, MessageEvent, MessageSegment
import json


@jjc_aomi_query.handle()
@connect_and_close_database
async def _jjc_aomi_query(bot: Bot, event: MessageEvent):
    """jjc奥秘+职业名"""
    try:
        with open(JJCCardsSetPath, "r", encoding="utf8") as fd:
            JJCCardsSet = json.loads(fd.read())["JJCCardsSet"]
    except:
        jjc_aomi_query.finish(f"程序错误，请联系系统管理员[QQ:{SYSTEM_ADMIN_QQ_NUMBER}]")
    for i in event.get_message():  # 获取该事件中每条消息
        print(i.data)
        if i.type == "text":  # 文本
            text_list = i.data['text'].split()
            print(text_list)
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
                    await jjc_aomi_query.send(message=message_str.strip())
                except: 
                    await jjc_aomi_query.send(message="您的输入有误，请输入“jjc奥秘 xxx”，例如“jjc奥秘 法师”")


@cards_query.handle()
@connect_and_close_database
async def _cards_query(bot: Bot, event: MessageEvent):
    """查卡牌+卡牌名"""
    for i in event.get_message():  # 获取该事件中每条消息
        print(i.data)
        if i.type == "text":  # 文本
            text_list = i.data['text'].split()
            print(text_list)
            if len(text_list) == 2:
                try:  # 卡牌名字、描述
                    card_text = text_list[1]
                    tep = find_card_by_text(card_text)
                    message_str = f"名称或描述中包含{card_text}的卡牌有:\n"
                    for i, j in enumerate(tep):
                        message_str += str(i + 1) + '. ' + j.name + '\n'
                    await cards_query.send(message=message_str.strip())
                except:  #
                    await cards_query.send(message="您的输入有误，请输入“查卡牌 xxx”，例如“查卡牌 叫嚣的中士”")


@minion_query.handle()
@connect_and_close_database
async def _minion_query(bot: Bot, event: MessageEvent):
    """查随从+身材"""
    for i in event.get_message():  # 获取该事件中每条消息
        print(i.data)
        if i.type == "text":  # 文本
            text_list = i.data['text'].split()
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
                            await minion_query.send(message=message_str.strip())
                        elif len(value_list) == 1:  # 类似"939" 不带 -
                            minion_cost = value_list[0][0]
                            minion_attack = value_list[0][1]
                            minion_health = value_list[0][2]
                            message_str = find_minion_by_body(
                                minion_cost, minion_attack, minion_health)
                            await minion_query.send(message=message_str.strip())
                        else:
                            await minion_query.send(message="您的输入有误，请输入“查随从 x-x-x”，例如“查随从 9-3-9”")
                    except:
                        await minion_query.send(message="您的输入有误，请输入“查随从 x-x-x”，例如“查随从 9-3-9”")

@jjc_choose.handle()
@connect_and_close_database
async def _jjc_choose(bot: Bot, event: MessageEvent):
    try:
        with open(JJCCardsSetPath, "r", encoding="utf8") as fd:
            JJCCardsSet = json.loads(fd.read())["JJCCardsSet"]
    except:
        jjc_choose.finish(f"程序错误，请联系系统管理员[QQ:{SYSTEM_ADMIN_QQ_NUMBER}]")
    for i in event.get_message():
        if i.type == 'text':
            text_list = i.data['text'].split()
            print(text_list)
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
                        await jjc_choose.send(message="网络连接不佳，请稍后再试")

                    #fp = open("jjc_winrate.json", "r", encoding="utf8")
                    #res_json = json.loads(fp.read())
                    
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
                        await jjc_choose.send(message=message_str.strip())

            else:
                await jjc_choose.send(message="您的输入有误，请输入“jjc选牌 <职业> <卡牌名>”，例如“jjc选牌 德 奇迹生长”")


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
    for i in event.get_message():
        if i.type == 'text':
            text_list = i.data['text'].split()
            if len(text_list) == 2:
                gametype = -1
                cardClassMap = {"法师": "MAGE", "猎人": "HUNTER", "牧师": "PRIEST", "术士": "WARLOCK", "潜行者": "ROGUE",
                                "德鲁伊": "DRUID", "萨满": "SHAMAN", "战士": "WARRIOR", "圣骑士": "PALADIN", "恶魔猎手": "DEMONHUNTER"}

                res_json = ask_json.get_performance_data()
                if res_json['status'] != 1:
                   await class_performance.send(message="网络连接不佳，请稍后再试")

                #fp = open("performance_data.json", "r", encoding="utf8")
                #res_json = json.loads(fp.read())

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
    """获取卡组图片"""
    for i in event.get_message():
        if i.type=='text':
            deck_text = ""
            pattern="AAE[BCD]A"
            result=re.search(pattern,i.data['text'])
            deck_code=""
            
            for l in range(result.regs[-1][0],len(i.data['text'])):
                if i.data['text'][l]!='\n':
                    deck_code+=i.data['text'][l]
            print(deck_code)
            
            deck_code = parse.quote(deck_code) #注意+转%2B这种情况
            url = f"https://hs.fbigame.com/decks.php?deck_code={deck_code}"
            req = requests.get(url=url)
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
                await build_cards.finish(message="hs.fbigame.com网站更新，未找到对应hash值，请通知管理员")


@pic_query.handle()
@connect_and_close_database
async def _pic_query(bot:Bot,event:MessageEvent):
    for message in event.get_message():
        if message.type=="text":
            text_list = message.data['text'].split()
            print(text_list)
            if len(text_list) > 1:
                for i in range(len(text_list) - 1):
                    try:
                        tep=models.Cards.get(models.Cards.name==text_list[i + 1])
                        url=f"https://art.hearthstonejson.com/v1/render/latest/zhCN/256x/{tep.id}.png"
                        print(tep.id)
                        resp=requests.get(url)
                        #img = base64.urlsafe_b64decode(resp._content)
                        await pic_query.send(message=MessageSegment.image(resp._content))
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
