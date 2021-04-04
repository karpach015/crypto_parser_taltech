import config
import asyncio
import logging

from aiogram import Bot, Dispatcher, executor, types
from Parser import MyParser

logging.basicConfig(level=logging.INFO)

bot = Bot(token=config.TOKEN)
dp = Dispatcher(bot)
parser = MyParser()


async def main(wait_for):
    i = 0
    while True:
        await asyncio.sleep(wait_for)

        with open('data.txt', 'a') as file:
            file.write(str(i) + ") " + str(parser.parse_coin_market()) + "\n")

        with open('data.txt', 'r') as file:
            x = str(file.readlines())
            logging.info(x)
        i += 1


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.create_task(main(2))
    executor.start_polling(dp, skip_updates=True)
