from nonebot import on_command, on_startswith
from nonebot.adapters.onebot.v11 import Bot, MessageEvent

import pypinyin
import csv

def get_translation(input, dict_path):
    # load dict
    with open(dict_path, "r", encoding='utf-8') as csv_file:
        reader=csv.reader(csv_file)
        word_dict=dict(reader)

    # get tones of words
    tones = pypinyin.pinyin(input, style=pypinyin.TONE)

    # translate
    output = ''
    for tone in tones:
        tone = tone[0]
        if tone in word_dict:
            output += word_dict[tone]
        else: # keep if not in dict
            output += tone
    
    return output
djwcb=on_startswith(msg=("生僻字转换 ","djw ","djwcb "),priority=1,block=True)
@djwcb.handle()
async def _djwcb(event:MessageEvent):
    for i in event.get_message():#获取该事件中每条消息
        if i.type=="text":#文本
            text_list=i.data['text'].split()
            if len(text_list)==2:
                dict_path="./src/plugins/djwcb_tran/word_dict.csv"
                res = get_translation(text_list[1], dict_path)
                await djwcb.send(message=res)
            else:
                await djwcb.send(message="您的输入有误，请输入“djw xxx”，例如“djw 戴佳伟菜逼”")
