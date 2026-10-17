import asyncio
import logging
from aiogram import Bot, Dispatcher, F
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import (
    ChatJoinRequest,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Message,
    WebAppInfo,
)
from aiogram.client.default import DefaultBotProperties

import config

logging.basicConfig(level=logging.INFO)
bot = Bot(
    token=config.BOT_TOKEN,
    default=DefaultBotProperties(parse_mode=ParseMode.MARKDOWN)
)
dp = Dispatcher()


def get_avatar_keyboard() -> InlineKeyboardMarkup:
    """Инлайн-клавиатура с кнопкой Web App и ссылкой на правила"""
    kb = [
        [
            InlineKeyboardButton(
                text="🌌 Открыть свиток клана (Web App)",
                web_app=WebAppInfo(url=config.WEBAPP_URL)
            )
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=kb)


@dp.message(CommandStart())
async def cmd_start(message: Message):
    greeting = (
        f"🌌 *Оэль нгати камейе, {message.from_user.first_name}!* (Я тебя вижу)\n\n"
        "Я хранитель священного древа и страж врат клана.\n"
        "Чтобы присоединиться к нашему пространству, перейди по ссылке-приглашению с заявкой.\n\n"
        "Перед входом ознакомься со священным свитком и подготовь анкету:"
    )
    await message.answer(greeting, reply_markup=get_avatar_keyboard())


@dp.chat_join_request()
async def handle_join_request(event: ChatJoinRequest):
    """
    Срабатывает в момент, когда пользователь нажимает кнопку
    вступления по ссылке с премодерацией заявок.
    """
    user_name = event.from_user.first_name
    user_id = event.from_user.id
    
    welcome_text = (
        f"💠 *Приветствуем у врат клана, {user_name}!* 💠\n\n"
        "Твоя заявка на подключение к древу духов получена.\n\n"
        "⚠️ *ВНИМАНИЕ! ПРАВИЛА ВСТУПЛЕНИЯ:* \n"
        "Сразу после принятия в чат отправь **анкету о себе одним сообщением** в общий чат. "
        "Анкеты, написанные не по формату, отклоняются советом клана.\n\n"
        "📋 *Шаблон анкеты для копирования:*\n"
        f"```\n{config.ANKETA_TEMPLATE}\n```\n\n"
        "Нажми кнопку ниже, чтобы открыть интерактивный свиток с правилами и скопировать форму в один тап."
    )

    try:
        # Отправляем памятку в личные сообщения пользователю
        await bot.send_message(
            chat_id=user_id,
            text=welcome_text,
            reply_markup=get_avatar_keyboard()
        )
        
        # Автоматическое одобрение заявки в чат
        # Если требуется ручная модерация админом - закомментируйте строку ниже:
        await event.approve()
        
    except Exception as e:
        logging.error(f"Не удалось отправить ЛС пользователю {user_id}: {e}")
        # Даже если ЛС закрыты, заявку можно одобрить
        await event.approve()


async def main():
    print("💠 Страж врат Пандоры запущен...")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())