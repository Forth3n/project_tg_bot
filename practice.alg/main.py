import asyncio
from aiogram import Bot, Dispatcher


from app.handlers import router
from app.database.models import async_main


async def main():
    await async_main()
    bot = Bot(token='7655734157:AAG7YCUrGD44LVX5CUusAy1NNEom-v2TiPQ')
    dp = Dispatcher()
    dp.include_router(router)
    await dp.start_polling(bot)


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("бот выкл")
