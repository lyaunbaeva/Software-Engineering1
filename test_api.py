"""
Скрипт для тестирования API калькулятора.
Можно использовать для проверки работоспособности всех эндпоинтов.
"""

import requests
import json

API_URL = "http://localhost:5000"
API_KEY = "secret_key_12345"

def print_response(title, response):
    """Красиво выводит ответ API."""
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}")
    print(f"Статус код: {response.status_code}")
    print(f"Ответ:")
    print(json.dumps(response.json(), indent=2, ensure_ascii=False))
    print(f"{'='*60}\n")

def test_health():
    """Тест проверки работоспособности."""
    print("🔍 Тест 1: Проверка работоспособности API")
    response = requests.get(f"{API_URL}/api/health")
    print_response("GET /api/health", response)
    return response.status_code == 200

def test_get_operations():
    """Тест получения списка операций."""
    print("🔍 Тест 2: Получение списка операций")
    headers = {"X-API-Key": API_KEY}
    response = requests.get(f"{API_URL}/api/operations", headers=headers)
    print_response("GET /api/operations", response)
    return response.status_code == 200

def test_calculate_add():
    """Тест сложения."""
    print("🔍 Тест 3: Выполнение сложения (10 + 5)")
    headers = {
        "Content-Type": "application/json",
        "X-API-Key": API_KEY
    }
    data = {
        "operation": "add",
        "a": 10,
        "b": 5
    }
    response = requests.post(
        f"{API_URL}/api/calculate",
        headers=headers,
        json=data
    )
    print_response("POST /api/calculate (add)", response)
    return response.status_code == 200 and response.json().get("result") == 15

def test_calculate_multiply():
    """Тест умножения."""
    print("🔍 Тест 4: Выполнение умножения (7 × 6)")
    headers = {
        "Content-Type": "application/json",
        "X-API-Key": API_KEY
    }
    data = {
        "operation": "multiply",
        "a": 7,
        "b": 6
    }
    response = requests.post(
        f"{API_URL}/api/calculate",
        headers=headers,
        json=data
    )
    print_response("POST /api/calculate (multiply)", response)
    return response.status_code == 200 and response.json().get("result") == 42

def test_calculate_divide():
    """Тест деления."""
    print("🔍 Тест 5: Выполнение деления (15 ÷ 3)")
    headers = {
        "Content-Type": "application/json",
        "X-API-Key": API_KEY
    }
    data = {
        "operation": "divide",
        "a": 15,
        "b": 3
    }
    response = requests.post(
        f"{API_URL}/api/calculate",
        headers=headers,
        json=data
    )
    print_response("POST /api/calculate (divide)", response)
    return response.status_code == 200 and response.json().get("result") == 5

def test_calculate_power():
    """Тест возведения в степень."""
    print("🔍 Тест 6: Выполнение возведения в степень (2^8)")
    headers = {
        "Content-Type": "application/json",
        "X-API-Key": API_KEY
    }
    data = {
        "operation": "power",
        "a": 2,
        "b": 8
    }
    response = requests.post(
        f"{API_URL}/api/calculate",
        headers=headers,
        json=data
    )
    print_response("POST /api/calculate (power)", response)
    return response.status_code == 200 and response.json().get("result") == 256

def test_divide_by_zero():
    """Тест обработки деления на ноль."""
    print("🔍 Тест 7: Обработка деления на ноль (10 ÷ 0)")
    headers = {
        "Content-Type": "application/json",
        "X-API-Key": API_KEY
    }
    data = {
        "operation": "divide",
        "a": 10,
        "b": 0
    }
    response = requests.post(
        f"{API_URL}/api/calculate",
        headers=headers,
        json=data
    )
    print_response("POST /api/calculate (divide by zero)", response)
    return response.status_code == 400

def test_get_history():
    """Тест получения истории."""
    print("🔍 Тест 8: Получение истории вычислений")
    headers = {"X-API-Key": API_KEY}
    response = requests.get(f"{API_URL}/api/history", headers=headers)
    print_response("GET /api/history", response)
    return response.status_code == 200

def test_delete_history_entry():
    """Тест удаления записи из истории."""
    print("🔍 Тест 9: Удаление записи из истории (ID: 1)")
    headers = {"X-API-Key": API_KEY}
    response = requests.delete(f"{API_URL}/api/history/1", headers=headers)
    print_response("DELETE /api/history/1", response)
    return response.status_code == 200

def test_invalid_api_key():
    """Тест с неверным API-ключом."""
    print("🔍 Тест 10: Проверка авторизации (неверный API-ключ)")
    headers = {
        "Content-Type": "application/json",
        "X-API-Key": "wrong_key"
    }
    data = {
        "operation": "add",
        "a": 10,
        "b": 5
    }
    response = requests.post(
        f"{API_URL}/api/calculate",
        headers=headers,
        json=data
    )
    print_response("POST /api/calculate (invalid API key)", response)
    return response.status_code == 401

def test_missing_fields():
    """Тест с отсутствующими полями."""
    print("🔍 Тест 11: Проверка валидации (отсутствует поле 'operation')")
    headers = {
        "Content-Type": "application/json",
        "X-API-Key": API_KEY
    }
    data = {
        "a": 10,
        "b": 5
    }
    response = requests.post(
        f"{API_URL}/api/calculate",
        headers=headers,
        json=data
    )
    print_response("POST /api/calculate (missing field)", response)
    return response.status_code == 400

def main():
    """Запуск всех тестов."""
    print("\n" + "="*60)
    print("  🧮 ТЕСТИРОВАНИЕ API КАЛЬКУЛЯТОРА")
    print("="*60)
    
    tests = [
        ("Проверка работоспособности", test_health),
        ("Получение списка операций", test_get_operations),
        ("Сложение", test_calculate_add),
        ("Умножение", test_calculate_multiply),
        ("Деление", test_calculate_divide),
        ("Возведение в степень", test_calculate_power),
        ("Деление на ноль", test_divide_by_zero),
        ("Получение истории", test_get_history),
        ("Удаление записи", test_delete_history_entry),
        ("Неверный API-ключ", test_invalid_api_key),
        ("Отсутствующие поля", test_missing_fields),
    ]
    
    results = []
    for name, test_func in tests:
        try:
            result = test_func()
            results.append((name, result))
        except requests.exceptions.ConnectionError:
            print(f"\n❌ ОШИБКА: Не удалось подключиться к {API_URL}")
            print("   Убедитесь, что API сервер запущен: python api.py\n")
            results.append((name, False))
            break
        except Exception as e:
            print(f"\n❌ ОШИБКА в тесте '{name}': {e}\n")
            results.append((name, False))
    
    # Итоги
    print("\n" + "="*60)
    print("  📊 РЕЗУЛЬТАТЫ ТЕСТИРОВАНИЯ")
    print("="*60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "✅ ПРОЙДЕН" if result else "❌ ПРОВАЛЕН"
        print(f"  {status}: {name}")
    
    print("="*60)
    print(f"  Всего тестов: {total}")
    print(f"  Пройдено: {passed}")
    print(f"  Провалено: {total - passed}")
    print(f"  Успешность: {passed/total*100:.1f}%")
    print("="*60 + "\n")

if __name__ == "__main__":
    main()
