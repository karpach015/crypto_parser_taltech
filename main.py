import config
import asyncio
import logging
import requests

from aiogram import Bot, Dispatcher, executor, types
from bs4 import BeautifulSoup as Bs

logging.basicConfig(level=logging.INFO)

bot = Bot(token=config.TOKEN)
dp = Dispatcher(bot)


async def get_new_urls(wait_for):
    parse_url = "https://assets.coingecko.com/sitemap1.xml"
    prev_urls = set()
    while True:
        await asyncio.sleep(wait_for)

        response = requests.get(parse_url)
        html = Bs(response.content, 'html.parser')


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.create_task(get_new_urls(2))
    executor.start_polling(dp, skip_updates=True)
