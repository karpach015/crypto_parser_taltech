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
        urls = set(Bs(response.content, 'html.parser').select("url loc"))

        if len(urls - prev_urls) > 0 and len(prev_urls) != 0:
            all_urls = [str(url.text) for url in (urls - prev_urls) if "/coins" in url.text]
            prev_urls = urls

            print(type(prev_urls[0]))
            print(type(urls[0]))

            urls_in_package_of_15 = []
            for i in range(len(all_urls) // 16 + 1):
                urls_in_package_of_15.append(all_urls[16*i:16*i+15])

            for urls_for_message in urls_in_package_of_15:
                message = "\n".join(urls_for_message)
                # print(message)
                await bot.send_message("-1001319115779", f"Новый ссылки:\n{message}")


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.create_task(get_new_urls(2))
    executor.start_polling(dp, skip_updates=True)
