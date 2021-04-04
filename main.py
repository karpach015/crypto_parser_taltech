import config
import asyncio
import logging
import time

from aiogram import Bot, Dispatcher, executor
from Parser import MyParser

logging.basicConfig(level=logging.INFO)

bot = Bot(token=config.TOKEN)
dp = Dispatcher(bot)
parser = MyParser()


async def main(wait_for):
    old_coins = {"coin_gecko": {},
                 "coin_market": {}}

    while True:
        start = time.time()

        skip_gecko = False
        skip_market = False

        await asyncio.sleep(wait_for)
        with open('data.txt', 'r') as file:
            temp = eval(file.readlines()[0])
            old_coins['coin_gecko'] = temp['coin_gecko']
            old_coins['coin_market'] = temp['coin_market']

        if len(old_coins['coin_gecko']) == 0:
            skip_gecko = True

        if len(old_coins['coin_market']) == 0:
            skip_market = True

        new_coin_gecko = parser.parse_sitemap_coin_gecko() - old_coins['coin_gecko']
        new_coin_market = parser.parse_coin_market() - old_coins['coin_market']
        new_coins = new_coin_gecko | new_coin_market

        if len(new_coins) > 0:
            [old_coins['coin_gecko'].add(coin) for coin in new_coin_gecko]
            [old_coins['coin_market'].add(coin) for coin in new_coin_market]
            with open('data.txt', 'w') as file:
                file.write(str(old_coins))

            if not skip_gecko and not skip_market:
                for new_coin in new_coins:
                    print(new_coin)
                    # await bot.send_message(config.CHAT_ID, new_coin)

            elif not skip_gecko:
                for new_coin in new_coin_gecko:
                    print(new_coin)
                    # await bot.send_message(config.CHAT_ID, new_coin)

            elif not skip_market:
                for new_coin in new_coin_market:
                    print(new_coin)
                    # await bot.send_message(config.CHAT_ID, new_coin)

        logging.info(f"Time passed {time.time() - start}")


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.create_task(main(1))
    executor.start_polling(dp, skip_updates=True)
