"""
Модуль для интеграции API калькулятора с Telegram-ботом.
Отправляет уведомления в Telegram при выполнении вычислений через API.
"""

import os
import asyncio
import logging
from telegram import Bot

logger = logging.getLogger(__name__)

# Получение токена бота из переменной окружения
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN', '')
# ID чата для отправки уведомлений (можно получить через @userinfobot)
DEFAULT_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID', '')


async def send_calculation_notification(expression: str, result: float, chat_id: str = None):
    """
    Отправляет уведомление о выполненном вычислении в Telegram.
    
    Args:
        expression: Строка с выражением (например, "10 + 5 = 15")
        result: Результат вычисления
        chat_id: ID чата для отправки (если не указан, используется DEFAULT_CHAT_ID)
    
    Returns:
        bool: True если уведомление отправлено успешно, False в противном случае
    """
    if not TELEGRAM_BOT_TOKEN:
        logger.warning("TELEGRAM_BOT_TOKEN не установлен. Уведомление не отправлено.")
        return False
    
    target_chat_id = chat_id or DEFAULT_CHAT_ID
    if not target_chat_id:
        logger.warning("TELEGRAM_CHAT_ID не установлен. Уведомление не отправлено.")
        return False
    
    try:
        bot = Bot(token=TELEGRAM_BOT_TOKEN)
        message = f"""
🧮 *Новое вычисление выполнено*

`{expression}`

*Результат:* `{result}`
"""
        await bot.send_message(
            chat_id=target_chat_id,
            text=message,
            parse_mode='Markdown'
        )
        logger.info(f"Уведомление отправлено в чат {target_chat_id}: {expression}")
        return True
    except Exception as e:
        logger.error(f"Ошибка при отправке уведомления в Telegram: {e}")
        return False


def send_notification_sync(expression: str, result: float, chat_id: str = None):
    """
    Синхронная обертка для отправки уведомления.
    Используется для интеграции с Flask API.
    """
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
    
    return loop.run_until_complete(
        send_calculation_notification(expression, result, chat_id)
    )


def get_chat_id_from_bot():
    """
    Вспомогательная функция для получения chat_id.
    Пользователь должен отправить сообщение боту, и эта функция поможет получить ID.
    """
    if not TELEGRAM_BOT_TOKEN:
        print("TELEGRAM_BOT_TOKEN не установлен!")
        return None
    
    async def get_updates():
        bot = Bot(token=TELEGRAM_BOT_TOKEN)
        updates = await bot.get_updates()
        if updates:
            chat_id = updates[-1].message.chat.id
            print(f"Ваш Chat ID: {chat_id}")
            return chat_id
        else:
            print("Нет обновлений. Отправьте сообщение боту и попробуйте снова.")
            return None
    
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
    
    return loop.run_until_complete(get_updates())


if __name__ == '__main__':
    # Вспомогательный скрипт для получения chat_id
    print("Получение Chat ID...")
    print("Отправьте любое сообщение вашему боту в Telegram")
    chat_id = get_chat_id_from_bot()
    if chat_id:
        print(f"\nСохраните этот ID в переменную окружения:")
        print(f"export TELEGRAM_CHAT_ID={chat_id}")
