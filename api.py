"""
REST API для калькулятора.
Предоставляет интерфейс для выполнения математических операций через HTTP запросы.
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
from calculator import add, subtract, multiply, divide, power
import os

app = Flask(__name__)
CORS(app)  # Разрешаем CORS для работы с фронтендом

# Простой API-ключ для авторизации 
API_KEY = os.getenv('CALCULATOR_API_KEY', 'secret_key_12345')

# История вычислений 
calculation_history = []
history_id_counter = 1


def validate_api_key():
    """Проверяет наличие и корректность API-ключа в заголовках запроса."""
    api_key = request.headers.get('X-API-Key')
    if not api_key or api_key != API_KEY:
        return jsonify({'error': 'Неверный или отсутствующий API-ключ'}), 401
    return None


@app.route('/api/health', methods=['GET'])
def health_check():
    """Проверка работоспособности API."""
    return jsonify({
        'status': 'ok',
        'message': 'API калькулятора работает',
        'version': '1.0'
    }), 200


@app.route('/api/operations', methods=['GET'])
def get_operations():
    """Получение списка доступных операций."""
    # Проверка API-ключа
    auth_error = validate_api_key()
    if auth_error:
        return auth_error
    
    operations = [
        {
            'name': 'addition',
            'symbol': '+',
            'description': 'Сложение двух чисел',
            'endpoint': '/api/calculate',
            'example': {'operation': 'add', 'a': 10, 'b': 5}
        },
        {
            'name': 'subtraction',
            'symbol': '-',
            'description': 'Вычитание второго числа из первого',
            'endpoint': '/api/calculate',
            'example': {'operation': 'subtract', 'a': 10, 'b': 5}
        },
        {
            'name': 'multiplication',
            'symbol': '*',
            'description': 'Умножение двух чисел',
            'endpoint': '/api/calculate',
            'example': {'operation': 'multiply', 'a': 10, 'b': 5}
        },
        {
            'name': 'division',
            'symbol': '/',
            'description': 'Деление первого числа на второе',
            'endpoint': '/api/calculate',
            'example': {'operation': 'divide', 'a': 10, 'b': 5}
        },
        {
            'name': 'power',
            'symbol': '^',
            'description': 'Возведение первого числа в степень второго',
            'endpoint': '/api/calculate',
            'example': {'operation': 'power', 'a': 2, 'b': 3}
        }
    ]
    
    return jsonify({
        'operations': operations,
        'total': len(operations)
    }), 200


@app.route('/api/calculate', methods=['POST'])
def calculate():
    """
    Выполнение математической операции.
    
    Формат запроса:
    {
        "operation": "add|subtract|multiply|divide|power",
        "a": число,
        "b": число
    }
    
    Формат ответа:
    {
        "result": результат,
        "operation": "add",
        "a": 10,
        "b": 5,
        "expression": "10 + 5 = 15",
        "id": 1
    }
    """
    # Проверка API-ключа
    auth_error = validate_api_key()
    if auth_error:
        return auth_error
    
    # Проверка наличия данных
    if not request.is_json:
        return jsonify({'error': 'Требуется JSON формат данных'}), 400
    
    data = request.get_json()
    
    # Валидация входных данных
    required_fields = ['operation', 'a', 'b']
    for field in required_fields:
        if field not in data:
            return jsonify({
                'error': f'Отсутствует обязательное поле: {field}'
            }), 400
    
    operation = data['operation'].lower()
    try:
        a = float(data['a'])
        b = float(data['b'])
    except (ValueError, TypeError):
        return jsonify({
            'error': 'Поля "a" и "b" должны быть числами'
        }), 400
    
    # Выполнение операции
    try:
        if operation == 'add':
            result = add(a, b)
            symbol = '+'
        elif operation == 'subtract':
            result = subtract(a, b)
            symbol = '-'
        elif operation == 'multiply':
            result = multiply(a, b)
            symbol = '*'
        elif operation == 'divide':
            result = divide(a, b)
            symbol = '/'
        elif operation == 'power':
            result = power(a, b)
            symbol = '^'
        else:
            return jsonify({
                'error': f'Неизвестная операция: {operation}',
                'available_operations': ['add', 'subtract', 'multiply', 'divide', 'power']
            }), 400
        
        # Форматирование результата
        if result == int(result):
            result = int(result)
        
        # Создание записи в истории
        global history_id_counter
        history_entry = {
            'id': history_id_counter,
            'operation': operation,
            'a': a,
            'b': b,
            'result': result,
            'expression': f'{a} {symbol} {b} = {result}'
        }
        calculation_history.append(history_entry)
        history_id_counter += 1
        
        # Формирование ответа
        response = {
            'result': result,
            'operation': operation,
            'a': a,
            'b': b,
            'expression': history_entry['expression'],
            'id': history_entry['id']
        }
        
        # Интеграция с Telegram: отправка уведомления (если настроено)
        telegram_enabled = os.getenv('TELEGRAM_ENABLED', 'false').lower() == 'true'
        if telegram_enabled:
            try:
                from telegram_integration import send_notification_sync
                chat_id = request.headers.get('X-Telegram-Chat-ID') or os.getenv('TELEGRAM_CHAT_ID')
                if chat_id:
                    send_notification_sync(history_entry['expression'], result, chat_id)
            except Exception as e:
                # Логируем ошибку, но не прерываем выполнение API
                import logging
                logging.error(f"Ошибка при отправке уведомления в Telegram: {e}")
        
        return jsonify(response), 200
        
    except ValueError as e:
        return jsonify({
            'error': str(e),
            'operation': operation,
            'a': a,
            'b': b
        }), 400
    except Exception as e:
        return jsonify({
            'error': f'Произошла ошибка при вычислении: {str(e)}'
        }), 500


@app.route('/api/history', methods=['GET'])
def get_history():
    """
    Получение истории вычислений.
    
    Параметры запроса (опционально):
    - limit: количество последних записей (по умолчанию все)
    """
    # Проверка API-ключа
    auth_error = validate_api_key()
    if auth_error:
        return auth_error
    
    limit = request.args.get('limit', type=int)
    
    if limit and limit > 0:
        history = calculation_history[-limit:]
    else:
        history = calculation_history
    
    return jsonify({
        'history': history,
        'total': len(calculation_history),
        'returned': len(history)
    }), 200


@app.route('/api/history/<int:history_id>', methods=['DELETE'])
def delete_history_entry(history_id):
    """
    Удаление записи из истории вычислений по ID.
    """
    # Проверка API-ключа
    auth_error = validate_api_key()
    if auth_error:
        return auth_error
    
    global calculation_history
    
    # Поиск записи по ID
    entry_to_delete = None
    for entry in calculation_history:
        if entry['id'] == history_id:
            entry_to_delete = entry
            break
    
    if not entry_to_delete:
        return jsonify({
            'error': f'Запись с ID {history_id} не найдена'
        }), 404
    
    # Удаление записи
    calculation_history.remove(entry_to_delete)
    
    return jsonify({
        'message': f'Запись с ID {history_id} успешно удалена',
        'deleted_entry': entry_to_delete
    }), 200


@app.route('/api/history', methods=['DELETE'])
def clear_history():
    """
    Очистка всей истории вычислений.
    """
    # Проверка API-ключа
    auth_error = validate_api_key()
    if auth_error:
        return auth_error
    
    global calculation_history
    count = len(calculation_history)
    calculation_history.clear()
    
    return jsonify({
        'message': f'История очищена. Удалено записей: {count}'
    }), 200


@app.errorhandler(404)
def not_found(error):
    """Обработка несуществующих эндпоинтов."""
    return jsonify({
        'error': 'Эндпоинт не найден',
        'available_endpoints': [
            'GET /api/health',
            'GET /api/operations',
            'POST /api/calculate',
            'GET /api/history',
            'DELETE /api/history/<id>',
            'DELETE /api/history'
        ]
    }), 404


@app.errorhandler(500)
def internal_error(error):
    """Обработка внутренних ошибок сервера."""
    return jsonify({
        'error': 'Внутренняя ошибка сервера'
    }), 500


if __name__ == '__main__':
    # Запуск сервера
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
    
    print(f"""
    ╔════════════════════════════════════════╗
    ║   🧮 API Калькулятора запущен          ║
    ╠════════════════════════════════════════╣
    ║   URL: http://localhost:{port}        ║
    ║   API Key: {API_KEY}                  ║
    ║   Debug: {debug}                      ║
    ╚════════════════════════════════════════╝
    
    Доступные эндпоинты:
    - GET  /api/health          - Проверка работоспособности
    - GET  /api/operations       - Список операций
    - POST /api/calculate        - Выполнение вычисления
    - GET  /api/history          - История вычислений
    - DELETE /api/history/<id>   - Удаление записи
    - DELETE /api/history        - Очистка истории
    
    Пример запроса:
    curl -X POST http://localhost:{port}/api/calculate \\
         -H "Content-Type: application/json" \\
         -H "X-API-Key: {API_KEY}" \\
         -d '{{"operation": "add", "a": 10, "b": 5}}'
    """)
    
    app.run(host='0.0.0.0', port=port, debug=debug)
