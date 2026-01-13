#!/bin/bash
# Скрипт для запуска Telegram-бота

export TELEGRAM_BOT_TOKEN=8515832260:AAFGin7b6P0q_6wPhbGmGuzLI87w1_JLmxo

echo "🤖 Запуск Telegram-бота калькулятора..."
echo "Токен установлен: ${TELEGRAM_BOT_TOKEN:0:20}..."
echo ""
echo "Бот будет запущен. Найдите его в Telegram и отправьте /start"
echo "Для остановки нажмите Ctrl+C"
echo ""

python telegram_bot.py
