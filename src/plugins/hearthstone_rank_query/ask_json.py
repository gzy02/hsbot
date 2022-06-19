import httpx

async def get_post_data(url: str, headers: dict, mode: int) -> dict:
    """
    :return: post data
    """
    async with httpx.AsyncClient() as client:
        res = dict()
        try:
            resp = await client.post(url, headers=headers, data={})
            resp_json = resp.json()
            if resp.status_code == 200:
                res['status'] = 1
                tepdic = resp_json['data'][mode]['seasons'][0]  # 始终找第一个
                tepdic.pop('dateKey')
                tepdic['type'] = resp_json['data'][mode]['type']
                res['data'] = tepdic
            else:
                res['status'] = 0
        except:
            res['status'] = 0
        return res


async def get_rank_data(url: str, headers: dict, data: dict) -> dict:
    """
    :return: rank data
    """
    async with httpx.AsyncClient() as client:
        res = dict()
        try:
            resp = await client.post(url, headers=headers, data=data)
            resp_json = resp.json()
            if resp.status_code == 200:
                res['status'] = 1
                res['data'] = resp_json['data']['ranks']
            else:
                res['status'] = 0
        except:
            res['status'] = 0
        return res
