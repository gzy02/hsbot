#tbot的核心插件
import openai
import json
openai.api_key = ''
openai.proxy="http://127.0.0.1:7890"#代理
async def ask_question(prompt):
    response = await openai.ChatCompletion.acreate(
        model="gpt-3.5-turbo",
        messages=prompt
    )
    return response['choices'][0]['message']['content'],response['usage']['total_tokens']


from nonebot import on_fullmatch, on_regex, on_startswith
from nonebot.adapters.onebot.v11 import MessageEvent,Bot
from nonebot.adapters.onebot.v11 import Bot, MessageEvent, MessageSegment, Message


#qq号json文件地址
qq_number_json_path = "./data_json/person.json"
#群组json文件地址
group_number_json_path = "./data_json/group.json"

user_session={}#用户id->prompt对应的list
group_session={}#qq群号->user_session
LIMIT_LEN_INPUT_TEXT=1000#输入限制

reset_query=on_fullmatch("重置会话", priority=1, block=False)
@reset_query.handle()
async def _reset_query(bot:Bot,event:MessageEvent):
    user_id=event.user_id
    #if event.message_type == "group":
    #    group_id=event.group_id
    #    if group_id in group_session:
    #        group_session[group_id][user_id]=[]
    #else:
    if event.message_type != "group":
        user_session[user_id]=[]
        await reset_query.send("重置成功")
        

set_query = on_startswith(msg=("#GPT设定 ","#gpt设定 "), priority=1, block=False)
@set_query.handle()
async def _set_query(bot: Bot ,event: MessageEvent):
    text = event.get_plaintext()[len("#GPT设定 "):]
    #if event.message_type == "group":
    #    if len(text)>LIMIT_LEN_INPUT_TEXT:
    #        await tj_query.send(message=MessageSegment.at(event.get_user_id())+"输入过长")
    #    group_id=event.group_id
    #    user_id=event.user_id
    #    try:
    #        #with open(group_number_json_path, "r", encoding="utf8") as #fd:
    #        #    qq_json = json.loads(fd.read())["group_qq_number"]
    #        #if group_id in qq_json:
    #        if group_id not in group_session:
    #            group_session[group_id]={}
    #        group_session[group_id][user_id]=[{"role":"system","content":text}]
    #        await set_query.send(MessageSegment.at(user_id)+"设定成功")
    #    except Exception as e:
    #        print(e)
    #        pass
    #else:
    if event.message_type != "group":
        user_id=event.user_id
        #with open(qq_number_json_path, "r", encoding="utf8") as fd:
        #    qq_json = json.loads(fd.read())["person_qq_number"]
        #if user_id in qq_json:
        user_session[user_id]=[{"role":"system","content":text}]
        await set_query.send("设定成功")

        
        
tj_query = on_startswith(msg=("#GPT ","#gpt "), priority=1, block=False)

async def getChatResponse(user_session:dict,user_id:int,text:str)->str:
    if user_id not in user_session:
        user_session[user_id]=[]
    user_session[user_id].append({"role": "user", "content": text})
    resp,total_token=await ask_question(user_session[user_id])
    if total_token<3500:
        user_session[user_id].append({"role": "assistant", "content":resp})
    else:
        await tj_query.send(message=MessageSegment.at(user_id)+"会话过长，会话已重置")
        user_session[user_id]=[]
    return resp

@tj_query.handle()
async def _tj_query(bot: Bot ,event: MessageEvent):
    text = event.get_plaintext()[len("#GPT "):]  #获取纯文本 去除表情和图片
    #if event.message_type == "group":
    #    if len(text)>LIMIT_LEN_INPUT_TEXT:
    #        await tj_query.send(message=MessageSegment.at(event.get_user_id())+"输入过长")
    #    group_id=event.group_id
    #    user_id=event.user_id
    #    try:
    #        #with open(group_number_json_path, "r", encoding="utf8") as fd:
    #        #    qq_json = json.loads(fd.read())["group_qq_number"]
    #        #if group_id in qq_json:
    #        if group_id not in group_session:
    #            group_session[group_id]={}
    #        resp=await getChatResponse(group_session[group_id],user_id,text)
    #        await tj_query.send(message=MessageSegment.at(user_id)+resp.strip())
    #    except Exception as e:
    #        group_session[group_id][user_id]=[]
    #        await tj_query.send(message=MessageSegment.at(user_id)+"与OpenAI的连接故障或会话过长，会话已重置")
    #        print(e)
    #        pass
    #else:
    if event.message_type != "group":
        try:
            user_id=event.user_id
            #with open(qq_number_json_path, "r", encoding="utf8") as fd:
            #    qq_json = json.loads(fd.read())["person_qq_number"]
            #if user_id in qq_json:
            resp=await getChatResponse(user_session,user_id,text)
            await tj_query.send(resp.strip())
        except Exception as e:
            user_session[user_id]=[]
            await tj_query.send(message=MessageSegment.at(user_id)+"与OpenAI的连接故障或会话过长，会话已重置")
            print(e)
