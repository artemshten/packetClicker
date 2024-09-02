import asyncio
from aiogram import Bot, Dispatcher, Router, F
from aiogram.types import Message, CallbackQuery, WebAppInfo
from aiogram.filters import CommandStart
from aiogram.enums import ParseMode
from aiogram.utils.keyboard import InlineKeyboardBuilder


def webapp_builder():
    builder = InlineKeyboardBuilder()
    builder.button(text='⚪️ Открыть игру', web_app=WebAppInfo(url='https://160d-109-237-12-246.ngrok-free.app'))
    return builder.as_markup()


router = Router()


@router.message(CommandStart())
async def start(message: Message):
    await message.reply('Привет!\nЛистинг уже не за горами, так что заходи и кликай пакеты',
                        reply_markup=webapp_builder())


async def main():
    bot = Bot('7528949580:AAE2tCNpzwqAEokJ44uXi4i4-EleVlhTePM')

    dp = Dispatcher()
    dp.include_router(router)

    await bot.delete_webhook(True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())