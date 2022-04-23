import httpx
from nonebot.log import logger
async def get_post_data(url:str,headers:dict,mode:int) -> dict:
    """
    :return: post data
    """
    async with httpx.AsyncClient() as client:
        res=dict()
        try:
            resp = await client.post(url, headers=headers,data={})
            resp_json=resp.json()
            if resp.status_code==200:
                res['status']=1
                tepdic=resp_json['data'][mode]['seasons'][0]#始终找第一个
                tepdic.pop('dateKey')
                tepdic['type']=resp_json['data'][mode]['type']
                res['data']=tepdic
            else:
                res['status']=0
        except:
            res['status']=0
        return res

async def get_rank_data(url:str,headers:dict,data:dict) -> dict:
    """
    :return: rank data
    """
    async with httpx.AsyncClient() as client:
        res=dict()
        try:
            resp = await client.post(url, headers=headers,data=data)
            resp_json=resp.json()
            if resp.status_code==200:
                res['status']=1
                res['data']=resp_json['data']['ranks']
            else:
                res['status']=0
        except:
            res['status']=0
            
        return res
        
async def solve(rank_query,keyword:str,mode:str):
    index_url = 'https://hs.blizzard.cn/action/hs/leaderboards/season/index'
    rank_url = 'https://hs.blizzard.cn/action/hs/leaderboards/season/rank'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36 Edg/100.0.1185.44'
    }
    mode_map={"标准":0,"狂野":1,"战棋":2,"经典":3,"佣兵":4}

    res_post_data=(await get_post_data(index_url,headers,mode_map[mode]))#标准是0
    if res_post_data['status']==1:
        res=(await get_rank_data(rank_url,headers,res_post_data['data']))
        if res['status']==1:
            found_list=[]
            for i in res['data']:
                if keyword in i['battleTag']:
                    found_list.append(i)
            res_str=f'{mode}月榜昵称包含{keyword}的ID有:\n'
            for i in range(len(found_list)):
                res_str+=f"{i+1}. {found_list[i]['battleTag']}\t排名：{found_list[i]['rank']}\n"
            await rank_query.send(message=res_str)
        else:
            logger.info('获取排名时出现错误')
    else:
        logger.info('获取排名前出现错误')
