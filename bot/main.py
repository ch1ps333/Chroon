from aiogram import Bot, Dispatcher
from handlers import bot_commands
from config import config as cfg
from middlewares.throttle import AntiFloodMiddleware
from datetime import date

import asyncio
import multiprocessing

def start_bot():
    asyncio.run(main())

async def main():
    bot = Bot(cfg.bot_token)
    dp = Dispatcher()

    dp.message.middleware(AntiFloodMiddleware(1.0))

    dp.include_routers (
        bot_commands.router,
    )

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    bot_process = multiprocessing.Process(target=start_bot)
    bot_process.start()
    bot_process.join()