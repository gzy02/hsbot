from nonebot import load_from_json, on_command,on_startswith
from nonebot.rule import to_me
from nonebot.adapters.onebot.v11 import Bot, MessageEvent, MessageSegment
from . import ask_json

rank_query=on_startswith(msg=("查标准","查狂野","查经典","查战棋","查战旗","查佣兵","查酒馆"),priority=1,block=False)
@rank_query.handle()
async def _rank_query(bot:Bot,event:MessageEvent):
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
            else:
                await rank_query.send(message="您的输入有误，请输入“查xx xxx”，例如“查标准 济往”")

def get_win_rate(gametype:int,res_json,cardClassMap)->str:
    res_list=[]
    for key,value in cardClassMap.items():
        for k in res_json['data'][value]:
            if k['game_type']==gametype:
                res_list.append([key,k['win_rate']])
                break
    res_list.sort(reverse=True,key=lambda x:x[1])
    message_str="模式下各职业胜率如下：\n"
    for i in res_list:
        message_str+=i[0]+': '+str(i[1])+'%\n'
    return message_str


import json
class_performance=on_startswith(msg=("查胜率"),priority=3,block=False)
@class_performance.handle()
async def _class_performance(bot:Bot,event:MessageEvent):
    for i in event.get_message():
        if i.type=='text':
            text_list=i.data['text'].split()
            if len(text_list)==2:
                gametype=-1
                cardClassMap={"法师":"MAGE","猎人":"HUNTER","牧师":"PRIEST","术士":"WARLOCK", "潜行者":"ROGUE", "德鲁伊":"DRUID", "萨满":"SHAMAN","战士": "WARRIOR", "圣骑士":"PALADIN", "恶魔猎手":"DEMONHUNTER"}
                
                #res_json=(await ask_json.get_performance_data())
                #if res_json['status']!=1:
                #    await class_performance.send(message="网络连接不佳，请稍后再试")
                fp=open("performance_data.json","r",encoding="utf8")
                res_json=json.loads(fp.read())
                res_json=res_json['series']
                if text_list[1]=="标准":
                    gametype=2
                    await class_performance.send(message= "标准"+get_win_rate(gametype,res_json,cardClassMap))
                elif text_list[1]=="狂野":
                    gametype=30
                    await class_performance.send(message= "狂野"+get_win_rate(gametype,res_json,cardClassMap))
                elif text_list[1]=="经典":#没有恶魔猎手
                    gametype=58
                    cardClassMap={"法师":"MAGE","猎人":"HUNTER","牧师":"PRIEST","术士":"WARLOCK", "潜行者":"ROGUE", "德鲁伊":"DRUID", "萨满":"SHAMAN","战士": "WARRIOR", "圣骑士":"PALADIN"}
                    await class_performance.send(message="经典" +get_win_rate(gametype,res_json,cardClassMap))
                elif text_list[1]=="竞技场" or text_list[1]=="jjc":
                    gametype=3
                    await class_performance.send(message= "竞技场"+get_win_rate(gametype,res_json,cardClassMap))
                elif text_list[1]=="对决":
                    gametype=55
                    await class_performance.send(message= "对决"+get_win_rate(gametype,res_json,cardClassMap))
                else:
                    await class_performance.send(message="您的输入有误，请输入“查胜率 xx”，例如“查胜率 jjc”")

            else:
                await class_performance.send(message="您的输入有误，请输入“查胜率 xx”，例如“查胜率 jjc”")

