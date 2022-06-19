from nonebot import on_command, on_startswith
from nonebot.adapters.onebot.v11 import Bot, Message,MessageEvent
import pypinyin
import csv
SYSTEM_ADMIN_QQ_NUMBER=1262454489

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
    try:
        text=event.get_plaintext()#获取纯文本 去除表情和图片
        state=0#初始状态
        newtext=""
        for i in text:
            if state==0 and i==' ':#读到空格
                state=1
            elif state==1 and i!=' ':
                state=2
                newtext+=i 
            elif state==2:
                newtext+=i

        dict_path="./src/plugins/djwcb_tran/word_dict.csv"
        res_str = get_translation(newtext, dict_path)
        if event.message_type=="group":
            res_str=f'[CQ:at,qq={event.get_user_id()}]'+res_str
        await djwcb.send(message=Message(res_str))

    except Exception as e:
        await djwcb.send(message=f'[djwcb]程序错误，请联系系统管理员[QQ:{SYSTEM_ADMIN_QQ_NUMBER}]\n错误如下：\n{repr(e)}')
