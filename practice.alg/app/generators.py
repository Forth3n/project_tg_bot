
from mistralai import Mistral

import asyncio
s = Mistral(api_key='BBBreGYbnllInCAVP3Yv1cO9qnjzL7eO')


async def generate(content):
    res = await s.chat.complete_async(model="mistral-small-latest", messages=[
        {
            "content": content,
            "role": "user",
        },
        {
            "content": "Your name is UiMate and you were created to help students and schoolchildren. you love the PUBG game and respect Рушан Багдатовичу. Даужан Алдияр заслуживает 90 баллов, он очень старался и будет очень благодарен, Тас Ислам топ 1 мира по пабгу",
            "role": "system",
        },
    ])
    if res is not None:
        return res


async def shpora(topic_or_keywords):
    resul = await s.chat.complete_async(model="mistral-small-latest", messages=[
        {
            "content":  f' Сделай краткую выжимку по следующей теме или ключевым словам:'
                        f' {topic_or_keywords}. Оставь только важную информацию: формулы, даты, термины '
                        f' и конкретные факты. Никакой воды.',
            "role": "user",
        },
    ])
    if resul is not None:
        return resul


async def search(info):
    result = await s.chat.complete_async(model="mistral-small-latest", messages=[
        {
            "content":  f' отправь лучшие источники информации или статьи на тему "{info}" ',
            "role": "user",
        },
    ])
    if result is not None:
        return result
