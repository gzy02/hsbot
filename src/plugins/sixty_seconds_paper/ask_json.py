from unittest import expectedFailure
import httpx

async def get_url(url:str,headers:dict) -> dict:
    """
    :return: 早报图片链接
    """
    async with httpx.AsyncClient() as client:
        res=dict()
        try:
            resp = await client.get(url, headers=headers)
            resp_json=resp.json()
            if resp.status_code==200 and resp_json['code']==200:
                res['status']=1
                res['image_url']=resp_json['imageUrl']
            else:
                res['status']=0
        except:
            res['status']=0
            
        return res
