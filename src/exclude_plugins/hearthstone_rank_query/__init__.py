from nonebot import load_from_json, on_command, on_startswith
from nonebot.rule import to_me
from nonebot.adapters.onebot.v11 import Bot, MessageEvent, Message
from nonebot.adapters.onebot.v11 import MessageEvent
from typing import Type
from nonebot.matcher import Matcher
from .ask_json import get_post_data, get_rank_data
import nonebot

driver = nonebot.get_driver()
global_config = driver.config
config = global_config.dict()
SYSTEM_ADMIN_QQ_NUMBER = config['system_admin_qq_number']

rank_query = on_startswith(msg=("查标准", "查狂野", "查经典", "查战棋", "查战旗", "查佣兵", "查酒馆"),
                           priority=1,
                           block=False)


async def solve(event: MessageEvent, rank_query: Type[Matcher], keyword: str, mode: str):
    index_url = 'https://hs.blizzard.cn/action/hs/leaderboards/season/index'
    rank_url = 'https://hs.blizzard.cn/action/hs/leaderboards/season/rank'
    headers = {
        'User-Agent':
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36 Edg/100.0.1185.44'
    }
    mode_map = {"标准": 0, "狂野": 1, "战棋": 2, "经典": 3, "佣兵": 4}

    # 标准是0
    res_post_data = (await get_post_data(index_url, headers, mode_map[mode]))
    if res_post_data['status'] == 1:
        res = (await get_rank_data(rank_url, headers, res_post_data['data']))
        if res['status'] == 1:
            found_list = []
            for i in res['data']:
                if keyword in i['battleTag']:
                    found_list.append(i)
            res_str = f'{mode}月榜昵称包含{keyword}的ID有:\n'
            for i in range(len(found_list)):
                res_str += f"{i+1}. {found_list[i]['battleTag']}\t排名：{found_list[i]['rank']}\n"
            if event.message_type == "group":
                res_str = f'[CQ:at,qq={event.get_user_id()}]' + res_str
            await rank_query.send(message=Message(res_str))
        else:
            await rank_query.send(
                message=f"hsbot与hs.blizzard.cn的网络连接不佳，请联系系统管理员[QQ:{SYSTEM_ADMIN_QQ_NUMBER}]")
    else:
        await rank_query.send(
            message=f"hsbot与hs.blizzard.cn的网络连接不佳，请联系系统管理员[QQ:{SYSTEM_ADMIN_QQ_NUMBER}]")


@rank_query.handle()
async def _rank_query(bot: Bot, event: MessageEvent):
    try:
        text = event.get_plaintext()  #获取纯文本 去除表情和图片
        text_list = text.split()
        if len(text_list) == 2:
            if text_list[0] == "查标准":
                await solve(event, rank_query, text_list[1], "标准")
            elif text_list[0] == "查狂野":
                await solve(event, rank_query, text_list[1], "狂野")
            elif text_list[0] == "查战棋" or text_list[0] == "查战旗" or text_list[0] == "查酒馆":
                await solve(event, rank_query, text_list[1], "战棋")
            elif text_list[0] == "查佣兵":
                await solve(event, rank_query, text_list[1], "佣兵")
            elif text_list[0] == "查经典":
                await solve(event, rank_query, text_list[1], "经典")
        else:
            await rank_query.send(message="您的输入有误，请输入“查xx xxx”，例如“查标准 济往”")
    except Exception as e:
        await rank_query.finish(f'[查榜单]程序错误，请联系系统管理员[QQ:{SYSTEM_ADMIN_QQ_NUMBER}]\n错误如下：\n{repr(e)}'
                                )
