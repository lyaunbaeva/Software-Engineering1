"""
Telegram-бот для калькулятора.
Интеграция с внешним сервисом Telegram для отправки уведомлений о вычислениях.
"""

import os
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from calculator import add, subtract, multiply, divide, power

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Получение токена бота из переменной окружения
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN', '')

# Словарь для хранения последних результатов пользователей
user_results = {}


def calculate_operation(operation, a, b):
    """Выполняет математическую операцию."""
    try:
        if operation == 'add' or operation == '+':
            result = add(a, b)
            symbol = '+'
        elif operation == 'subtract' or operation == '-':
            result = subtract(a, b)
            symbol = '-'
        elif operation == 'multiply' or operation == '*' or operation == '×':
            result = multiply(a, b)
            symbol = '×'
        elif operation == 'divide' or operation == '/' or operation == '÷':
            result = divide(a, b)
            symbol = '÷'
        elif operation == 'power' or operation == '^' or operation == '**':
            result = power(a, b)
            symbol = '^'
        else:
            return None, None, "Неизвестная операция"
        
        return result, symbol, None
    except ValueError as e:
        return None, None, str(e)
    except Exception as e:
        return None, None, f"Ошибка: {str(e)}"


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик команды /start."""
    welcome_message = """
🧮 *Добро пожаловать в Калькулятор-бот!*

Я могу выполнять математические операции и отправлять результаты.

*Доступные команды:*
/start - Показать это сообщение
/help - Справка по использованию
/calculate - Выполнить вычисление
/history - Показать последний результат

*Примеры использования:*
• Отправьте: `10 + 5`
• Отправьте: `15 / 3`
• Отправьте: `2 ^ 8`
• Или используйте команду: /calculate 10 + 5
"""
    await update.message.reply_text(welcome_message, parse_mode='Markdown')


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик команды /help."""
    help_text = """
📖 *Справка по использованию калькулятора*

*Доступные операции:*
➕ Сложение: `+` или `add`
➖ Вычитание: `-` или `subtract`
✖️ Умножение: `*`, `×` или `multiply`
➗ Деление: `/`, `÷` или `divide`
🔢 Степень: `^`, `**` или `power`

*Способы использования:*

1. *Простой ввод:*
   Отправьте сообщение в формате: `число операция число`
   Пример: `10 + 5`

2. *Команда /calculate:*
   `/calculate 10 + 5`
   `/calculate 2 ^ 8`

3. *Десятичные числа:*
   `3.5 + 2.7`

4. *Отрицательные числа:*
   `-5 + 3`

*Примеры:*
• `15 + 27` → 42
• `100 / 4` → 25
• `7 × 6` → 42
• `2 ^ 10` → 1024
"""
    await update.message.reply_text(help_text, parse_mode='Markdown')


async def calculate_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик команды /calculate."""
    if not context.args:
        await update.message.reply_text(
            "❌ Использование: /calculate <число1> <операция> <число2>\n"
            "Пример: /calculate 10 + 5"
        )
        return
    
    try:
        # Парсинг аргументов
        if len(context.args) < 3:
            raise ValueError("Недостаточно аргументов")
        
        a = float(context.args[0])
        operation = context.args[1].lower()
        b = float(context.args[2])
        
        result, symbol, error = calculate_operation(operation, a, b)
        
        if error:
            await update.message.reply_text(f"❌ {error}")
        else:
            expression = f"{a} {symbol} {b} = {result}"
            message = f"✅ *Результат:*\n`{expression}`"
            
            # Сохранение результата
            user_id = update.effective_user.id
            user_results[user_id] = {
                'expression': expression,
                'result': result,
                'a': a,
                'b': b,
                'operation': operation
            }
            
            await update.message.reply_text(message, parse_mode='Markdown')
            
    except ValueError as e:
        await update.message.reply_text(f"❌ Ошибка: {str(e)}\nИспользование: /calculate <число1> <операция> <число2>")


async def history_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик команды /history - показывает последний результат."""
    user_id = update.effective_user.id
    
    if user_id in user_results:
        result = user_results[user_id]
        message = f"📊 *Последний результат:*\n`{result['expression']}`"
        await update.message.reply_text(message, parse_mode='Markdown')
    else:
        await update.message.reply_text("ℹ️ У вас пока нет истории вычислений.")


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик текстовых сообщений для автоматического вычисления."""
    text = update.message.text.strip()
    
    # Попытка распарсить выражение вида "10 + 5" или "15/3"
    try:
        # Поддержка различных форматов
        text = text.replace('×', '*').replace('÷', '/').replace('^', '**')
        
        # Простой парсинг для формата "число операция число"
        parts = text.split()
        if len(parts) == 3:
            a = float(parts[0])
            operation = parts[1].lower()
            b = float(parts[2])
            
            result, symbol, error = calculate_operation(operation, a, b)
            
            if error:
                await update.message.reply_text(f"❌ {error}")
            else:
                expression = f"{a} {symbol} {b} = {result}"
                message = f"✅ *Результат:*\n`{expression}`"
                
                # Сохранение результата
                user_id = update.effective_user.id
                user_results[user_id] = {
                    'expression': expression,
                    'result': result,
                    'a': a,
                    'b': b,
                    'operation': operation
                }
                
                await update.message.reply_text(message, parse_mode='Markdown')
        else:
            # Если не удалось распарсить, предлагаем помощь
            await update.message.reply_text(
                "❓ Не понял ваш запрос.\n\n"
                "Отправьте выражение в формате: `число операция число`\n"
                "Пример: `10 + 5`\n\n"
                "Или используйте команду /help для справки.",
                parse_mode='Markdown'
            )
    except (ValueError, IndexError):
        await update.message.reply_text(
            "❓ Не удалось распознать выражение.\n\n"
            "Используйте формат: `число операция число`\n"
            "Пример: `10 + 5`\n\n"
            "Команда /help покажет все возможности.",
            parse_mode='Markdown'
        )


async def send_notification(chat_id: int, message: str, bot_token: str = None):
    """
    Отправляет уведомление в Telegram.
    Используется для интеграции с API.
    """
    if not bot_token:
        bot_token = TELEGRAM_BOT_TOKEN
    
    if not bot_token:
        logger.warning("TELEGRAM_BOT_TOKEN не установлен. Уведомление не отправлено.")
        return False
    
    try:
        from telegram import Bot
        bot = Bot(token=bot_token)
        await bot.send_message(chat_id=chat_id, text=message, parse_mode='Markdown')
        logger.info(f"Уведомление отправлено в чат {chat_id}")
        return True
    except Exception as e:
        logger.error(f"Ошибка при отправке уведомления: {e}")
        return False


def main():
    """Запуск Telegram-бота."""
    if not TELEGRAM_BOT_TOKEN:
        print("""
        ⚠️  ОШИБКА: TELEGRAM_BOT_TOKEN не установлен!
        
        Для запуска бота необходимо:
        1. Создать бота через @BotFather в Telegram
        2. Получить токен бота
        3. Установить переменную окружения:
           export TELEGRAM_BOT_TOKEN=your_bot_token_here
        
        Или запустите:
        TELEGRAM_BOT_TOKEN=your_token python telegram_bot.py
        """)
        return
    
    print(f"""
    ╔════════════════════════════════════════╗
    ║   🤖 Telegram-бот калькулятора         ║
    ╠════════════════════════════════════════╣
    ║   Бот запущен и готов к работе!       ║
    ║   Найдите вашего бота в Telegram       ║
    ╚════════════════════════════════════════╝
    """)
    
    # Создание приложения
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
    
    # Регистрация обработчиков
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("calculate", calculate_command))
    application.add_handler(CommandHandler("history", history_command))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    # Запуск бота
    logger.info("Бот запущен")
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == '__main__':
    main()
