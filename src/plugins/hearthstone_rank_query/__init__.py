from nonebot import on_command,on_startswith
from nonebot.rule import to_me
from nonebot.adapters.onebot.v11 import Bot, MessageEvent, MessageSegment
from . import ask_json

rank_query=on_startswith(msg=("查标准","查狂野","查经典","查战棋","查战旗","查佣兵","查酒馆"),priority=1,block=False)
@rank_query.handle()
async def _(bot:Bot,event:MessageEvent):
    for i in event.get_message():#获取该事件中每条消息
        print(i.data)
        if i.type=="text":#文本
            text_list=i.data['text'].split()
            if len(text_list)==2:
                if text_list[0]=="查标准":
                    await ask_json.solve(rank_query,text_list[1],"标准")
                elif text_list[0]=="查狂野":
                    await ask_json.solve(rank_query,text_list[1],"狂野")
                elif text_list[0]=="查战棋" or text_list[0]=="查战旗" or text_list[0]=="查酒馆":
                    await ask_json.solve(rank_query,text_list[1],"战棋")
                elif text_list[0]=="查佣兵":
                    await ask_json.solve(rank_query,text_list[1],"佣兵")
                elif text_list[0]=="查经典":
                    await ask_json.solve(rank_query,text_list[1],"经典")
