from . import models
import peewee

def find_minion_by_body(minion_cost, minion_attack, minion_health) -> str:
    tep = models.Cards.select(models.Cards.name, models.Cards.text).join(models.MINIONCards).where(  # type: ignore
        models.Cards.dbfid == models.MINIONCards.Cardid, models.MINIONCards.cost == minion_cost, models.MINIONCards.attack == minion_attack, models.MINIONCards.health == minion_health)
    message_str = f"身材为{minion_cost}-{minion_attack}-{minion_health}的随从有:\n"
    for i, j in enumerate(tep):
        message_str += str(i + 1) + '. ' + j.name + '\n'
    return message_str


def find_card_by_text(text: str)->peewee.ModelSelect: 
    return models.Cards.select(models.Cards.name,models.Cards.cardClass, models.Cards.dbfid, models.Cards.id, models.Cards.text,models.Cards.set).where((models.Cards.name.contains(text) | models.Cards.text.contains(text)))


import httpx
async def get_jjc_data() -> dict:
    """
    :return: jjc data
    """
    url = 'https://hsreplay.net/analytics/query/card_list_free/?GameType=ARENA&TimeRange=CURRENT_PATCH'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36 Edg/100.0.1185.44'
    }
    async with httpx.AsyncClient() as client:
        res=dict()
        try:
            resp = await client.get(url, headers=headers)
            resp_json=resp.json()
            if resp.status_code==200:
                res['status']=1
                res['data']=resp_json['series']['data']
            else:
                res['status']=0
        except:
            res['status']=0
            
        return res
        