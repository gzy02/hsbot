from .utility import connect_and_close_database, cardClassMap, aliasesClassMap, JJCCardsSetPath, SYSTEM_ADMIN_QQ_NUMBER
from . import jjc_choose, build_cards, pic_query
from . import models
from .query import find_card_by_name
from . import ask_json
from nonebot.adapters.onebot.v11 import Bot, MessageEvent, MessageSegment, Message
import json
import re
from typing import Tuple
import base64
from urllib import parse
import requests
from PIL import Image
from io import BytesIO
import matplotlib.pyplot as plt


def Get_jjc_image(rowLabels: list, cellText: list):
    """获取图片"""
    plt.rcParams['font.sans-serif'] = ['SimHei']  #字体
    fig = plt.figure(figsize=(7, len(rowLabels) / 2))  #调比例，还可根据胜率排个序
    print(rowLabels)
    table = plt.table(cellText=cellText,
                      rowLabels=rowLabels,
                      loc='center',
                      cellLoc='center',
                      rowLoc='center')
    table.auto_set_font_size(False)
    table.auto_set_column_width(col=list(range(len(cellText[0]) + 1)))
    table.set_fontsize(10)  #字体大小
    table.scale(1, 2)  #表格缩放
    plt.axis('off')
    canvas = fig.canvas
    buffer = BytesIO()
    canvas.print_png(buffer)
    data = buffer.getvalue()
    return data


@jjc_choose.handle()
@connect_and_close_database
async def _jjc_choose(bot: Bot, event: MessageEvent):
    "jjc选牌+卡牌名列表"
    try:
        with open(JJCCardsSetPath, "r", encoding="utf8") as fd:
            JJCCardsSet = json.loads(fd.read())["JJCCardsSet"]
    except Exception as e:
        jjc_choose.finish(f"[jjc选牌]程序错误，请联系系统管理员[QQ:{SYSTEM_ADMIN_QQ_NUMBER}]\n错误如下：\n{repr(e)}")
    try:
        text = event.get_plaintext()  #获取纯文本 去除表情和图片
        text_list = text.split()
        if len(text_list) > 2:
            # 别名，不指定则默认全职业
            cardClassMap = {
                "全职业": "ALL",
                "法师": "MAGE",
                "猎人": "HUNTER",
                "牧师": "PRIEST",
                "术士": "WARLOCK",
                "潜行者": "ROGUE",
                "德鲁伊": "DRUID",
                "萨满祭司": "SHAMAN",
                "战士": "WARRIOR",
                "圣骑士": "PALADIN",
                "恶魔猎手": "DEMONHUNTER"
            }
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

                    need = [
                        models.Cards.name, models.Cards.cardClass, models.Cards.dbfid,
                        models.Cards.id, models.Cards.text, models.Cards.set
                    ]
                    found = False

                    teps = models.Cards.select(*need).where(models.Cards.name == text_list[i + 2])
                    for tep in teps:
                        if tep.set in JJCCardsSet:
                            query_dir[tep.dbfid] = tep.name
                            found = True
                            break
                    if found == False:
                        tep = find_card_by_name(text_list[i + 2])
                        for j in tep:
                            if j.set in JJCCardsSet:  # 当前jjc套牌池
                                query_dir[j.dbfid] = j.name

                res_json = ask_json.get_jjc_data()
                if res_json['status'] != 1:
                    await jjc_choose.send(
                        message=f"hsbot与hsreplay的网络连接不佳，请联系系统管理员[QQ:{SYSTEM_ADMIN_QQ_NUMBER}]")
                    #或者读取本地
                    #fp = open("jjc_winrate.json", "r", encoding="utf8")
                    #res_json = json.loads(fp.read())
                else:
                    res_json = res_json['series']
                    message_head = "以上卡牌的jjc数据如下：\n"
                    max_winrate = 0
                    recommand_card = ""
                    rowLabels = ["卡牌名"]  #卡牌名列表
                    cellText = [["包含胜率", "打出胜率", "出现概率", "平均张数", "打出次数"]]  #相应数据
                    for item in res_json['data'][cur_class]:
                        if item['dbf_id'] in query_dir:
                            if item['included_winrate'] > max_winrate:
                                max_winrate = item['included_winrate']
                                recommand_card = query_dir[item['dbf_id']]
                            cellText_sub = []
                            rowLabels.append(query_dir[item['dbf_id']])
                            cellText_sub.append(str(item['included_winrate']))
                            cellText_sub.append(str(item['winrate_when_played']))
                            cellText_sub.append(str(item['included_popularity']))
                            cellText_sub.append(str(item['included_count']))
                            cellText_sub.append(str(item['times_played']))
                            cellText.append(cellText_sub)
                    if recommand_card == "":
                        message = "未在当前jjc卡池中找到您的输入卡牌，请重新输入"
                        if event.message_type == "group":
                            message = MessageSegment.at(event.get_user_id()) + message
                        await jjc_choose.send(message=message)
                    else:
                        recommand_card_str = "\n推荐选取：" + recommand_card
                        img_data = Get_jjc_image(rowLabels, cellText)
                        if event.message_type == "group":
                            message_head = MessageSegment.at(event.get_user_id()) + message_head
                        await jjc_choose.send(message_head + MessageSegment.image(img_data) +
                                              recommand_card_str)
        else:
            await jjc_choose.send(message="您的输入有误，请输入“jjc选牌 <职业> <卡牌名>”，例如“jjc选牌 德 奇迹生长”")
    except Exception as e:
        await jjc_choose.finish(
            f'[jjc选牌]程序错误，请联系系统管理员[QQ:{SYSTEM_ADMIN_QQ_NUMBER}]\n错误如下：\n{repr(e)}')


def gethash(text: str) -> Tuple[bool, str]:
    """获取卡组图片的工具函数"""
    result = re.search('var hash = "(?P<hash>.*?)";', text)
    if result:
        return True, result.groupdict().get("hash")
    else:
        return False, "Not Found"


@build_cards.handle()
async def _build_cards(bot: Bot, event: MessageEvent):
    """无需指令主动触发，自动判断收到信息中是否含有炉石代码，详见https://zhuanlan.zhihu.com/p/142113610"""
    #获取卡组图片，可以先解析然后用PIL库拼接图片。不过对PIL库不是很熟，这里先调fbigame的库了
    try:
        text = event.get_plaintext()  #获取纯文本 去除表情和图片
        deck_text = ""
        pattern = "AAE[BCD]A"
        result = re.search(pattern, text)
        deck_code = ""

        for l in range(result.regs[-1][0], len(text)):
            if text[l] != '\n':
                deck_code += text[l]

        deck_code = parse.quote(deck_code)  #注意+转%2B这种情况
        url = f"https://hs.fbigame.com/decks.php?deck_code={deck_code}"
        req = requests.get(url=url)
        if req.status_code == 200:
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
                    cropped = PIL_img.crop((0, 0, PIL_img.size[0], PIL_img.size[1] - 70))  # 裁剪图片
                    img_byte = BytesIO()
                    cropped.save(img_byte, format='PNG')
                    binary_str2 = img_byte.getvalue()
                    await build_cards.send(message=MessageSegment.image(binary_str2))
                else:
                    #非用户主动触发的指令就别向用户提示错误了，感觉没必要
                    pass
                    #await build_cards.send(
                    #    message = f"hsbot未获取hs.fbigame.com对应hash凭证，请联系系统管理员[QQ:{SYSTEM_ADMIN_QQ_NUMBER}]"
                    #)
        else:
            #非用户主动触发的指令就别向用户提示错误了，感觉没必要
            pass
            #await build_cards.send(
            #    message = f"hsbot与hs.fbigame.com的网络连接不佳，请联系系统管理员[QQ:{SYSTEM_ADMIN_QQ_NUMBER}]"
            #)
    except Exception as e:
        #非用户主动触发的指令就别向用户提示错误了，感觉没必要
        pass
        #await build_cards.finish(
        #    f'[卡组代码解析]程序错误，请联系系统管理员[QQ:{SYSTEM_ADMIN_QQ_NUMBER}]\n错误如下：\n{repr(e)}'
        #)


@pic_query.handle()
@connect_and_close_database
async def _pic_query(bot: Bot, event: MessageEvent):
    try:
        text = event.get_plaintext()  #获取纯文本 去除表情和图片
        text_list = text.split()
        if len(text_list) > 1:
            for i in range(len(text_list) - 1):
                try:
                    tep = models.Cards.get(models.Cards.name == text_list[i + 1])
                    url = f"https://art.hearthstonejson.com/v1/render/latest/zhCN/256x/{tep.id}.png"
                    resp = requests.get(url)
                    if resp.status_code == 200:
                        await pic_query.send(message=MessageSegment.image(resp._content))
                    else:
                        await build_cards.send(
                            message=
                            f"hsbot与art.hearthstonejson.com的网络连接不佳，请联系系统管理员[QQ:{SYSTEM_ADMIN_QQ_NUMBER}]"
                        )
                except:
                    tep = find_card_by_name(text_list[i + 1])
                    if tep.count() <= 0:
                        await pic_query.send(message="您的输入有误，请输入“查描述/查卡图 <卡牌名列表>”，例如“查描述 银背族长”")

                    for j in tep:
                        url = f"https://art.hearthstonejson.com/v1/render/latest/zhCN/256x/{j.id}.png"
                        resp = requests.get(url)
                        await pic_query.send(
                            message=f"检测到输入卡牌名并非完整全称，仅显示符合名称包含{text_list[i+1]}的其中一张" +
                            MessageSegment.image(resp._content))
                        break
        else:
            await pic_query.send(message="您的输入有误，请输入“查卡图 <卡牌名>”，例如“查卡图 银背族长”")
    except Exception as e:
        await build_cards.finish(
            f'[卡组代码解析]程序错误，请联系系统管理员[QQ:{SYSTEM_ADMIN_QQ_NUMBER}]\n错误如下：\n{repr(e)}')
