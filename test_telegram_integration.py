"""
Тесты для интеграции с Telegram.
Проверяет отправку уведомлений и обработку ошибок.
"""

import os
import unittest
from unittest.mock import patch, MagicMock, AsyncMock
import asyncio

# Импорт модулей для тестирования
from telegram_integration import send_calculation_notification, send_notification_sync


class TestTelegramIntegration(unittest.TestCase):
    """Тесты для интеграции с Telegram."""
    
    def setUp(self):
        """Настройка перед каждым тестом."""
        self.test_expression = "10 + 5 = 15"
        self.test_result = 15.0
        self.test_chat_id = "123456789"
    
    @patch('telegram_integration.TELEGRAM_BOT_TOKEN', 'test_token')
    @patch('telegram_integration.Bot')
    def test_send_notification_success(self, mock_bot_class):
        """Тест успешной отправки уведомления."""
        # Настройка мока
        mock_bot = AsyncMock()
        mock_bot_class.return_value = mock_bot
        mock_bot.send_message = AsyncMock(return_value=MagicMock())
        
        # Выполнение
        result = asyncio.run(
            send_calculation_notification(
                self.test_expression,
                self.test_result,
                self.test_chat_id
            )
        )
        
        # Проверка
        self.assertTrue(result)
        mock_bot.send_message.assert_called_once()
    
    @patch('telegram_integration.TELEGRAM_BOT_TOKEN', '')
    def test_send_notification_no_token(self):
        """Тест отправки без токена."""
        result = asyncio.run(
            send_calculation_notification(
                self.test_expression,
                self.test_result,
                self.test_chat_id
            )
        )
        self.assertFalse(result)
    
    @patch('telegram_integration.TELEGRAM_BOT_TOKEN', 'test_token')
    @patch('telegram_integration.Bot')
    def test_send_notification_error_handling(self, mock_bot_class):
        """Тест обработки ошибок при отправке."""
        # Настройка мока для выброса исключения
        mock_bot = AsyncMock()
        mock_bot_class.return_value = mock_bot
        mock_bot.send_message = AsyncMock(side_effect=Exception("Network error"))
        
        # Выполнение
        result = asyncio.run(
            send_calculation_notification(
                self.test_expression,
                self.test_result,
                self.test_chat_id
            )
        )
        
        # Проверка, что ошибка обработана корректно
        self.assertFalse(result)
    
    def test_send_notification_sync_wrapper(self):
        """Тест синхронной обертки."""
        with patch('telegram_integration.send_calculation_notification') as mock_async:
            mock_async.return_value = asyncio.coroutine(lambda: True)()
            result = send_notification_sync(
                self.test_expression,
                self.test_result,
                self.test_chat_id
            )
            # Проверка, что функция вызвана
            mock_async.assert_called_once()


class TestTelegramBot(unittest.TestCase):
    """Тесты для Telegram-бота."""
    
    def test_calculate_operation_add(self):
        """Тест операции сложения."""
        from telegram_bot import calculate_operation
        result, symbol, error = calculate_operation('add', 10, 5)
        self.assertEqual(result, 15)
        self.assertEqual(symbol, '+')
        self.assertIsNone(error)
    
    def test_calculate_operation_divide_by_zero(self):
        """Тест обработки деления на ноль."""
        from telegram_bot import calculate_operation
        result, symbol, error = calculate_operation('divide', 10, 0)
        self.assertIsNone(result)
        self.assertIsNotNone(error)
        self.assertIn('ноль', error.lower())


if __name__ == '__main__':
    unittest.main()
