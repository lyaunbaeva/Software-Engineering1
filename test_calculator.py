"""
Модульные тесты для калькулятора.

Тесты проверяют корректность работы всех функций калькулятора:
- Сложение (add)
- Вычитание (subtract)
- Умножение (multiply)
- Деление (divide)
- Возведение в степень (power)
"""

import unittest
from calculator import add, subtract, multiply, divide, power


class TestCalculator(unittest.TestCase):
    """Тестовый класс для функций калькулятора."""
    
    # ========== Тесты функции add (сложение) ==========
    
    def test_add_positive_numbers(self):
        """Тест сложения положительных чисел."""
        self.assertEqual(add(2, 3), 5)
        self.assertEqual(add(10, 20), 30)
        self.assertEqual(add(100, 50), 150)
    
    def test_add_negative_numbers(self):
        """Тест сложения отрицательных чисел."""
        self.assertEqual(add(-5, -3), -8)
        self.assertEqual(add(-10, -20), -30)
    
    def test_add_mixed_numbers(self):
        """Тест сложения положительных и отрицательных чисел."""
        self.assertEqual(add(-1, 1), 0)
        self.assertEqual(add(5, -3), 2)
        self.assertEqual(add(-10, 15), 5)
    
    def test_add_with_zero(self):
        """Тест сложения с нулем."""
        self.assertEqual(add(0, 0), 0)
        self.assertEqual(add(5, 0), 5)
        self.assertEqual(add(0, -5), -5)
    
    def test_add_float_numbers(self):
        """Тест сложения дробных чисел."""
        self.assertAlmostEqual(add(2.5, 3.7), 6.2, places=7)
        self.assertAlmostEqual(add(0.1, 0.2), 0.3, places=7)
    
    # ========== Тесты функции subtract (вычитание) ==========
    
    def test_subtract_positive_numbers(self):
        """Тест вычитания положительных чисел."""
        self.assertEqual(subtract(5, 3), 2)
        self.assertEqual(subtract(10, 7), 3)
    
    def test_subtract_negative_numbers(self):
        """Тест вычитания отрицательных чисел."""
        self.assertEqual(subtract(-2, -3), 1)
        self.assertEqual(subtract(-5, -2), -3)
    
    def test_subtract_mixed_numbers(self):
        """Тест вычитания с смешанными знаками."""
        self.assertEqual(subtract(5, -3), 8)
        self.assertEqual(subtract(-5, 3), -8)
    
    def test_subtract_with_zero(self):
        """Тест вычитания с нулем."""
        self.assertEqual(subtract(0, 5), -5)
        self.assertEqual(subtract(10, 0), 10)
        self.assertEqual(subtract(10, 10), 0)
    
    def test_subtract_float_numbers(self):
        """Тест вычитания дробных чисел."""
        self.assertAlmostEqual(subtract(5.5, 2.3), 3.2, places=7)
    
    # ========== Тесты функции multiply (умножение) ==========
    
    def test_multiply_positive_numbers(self):
        """Тест умножения положительных чисел."""
        self.assertEqual(multiply(3, 4), 12)
        self.assertEqual(multiply(10, 5), 50)
    
    def test_multiply_negative_numbers(self):
        """Тест умножения отрицательных чисел."""
        self.assertEqual(multiply(-3, -4), 12)
        self.assertEqual(multiply(-2, -5), 10)
    
    def test_multiply_mixed_numbers(self):
        """Тест умножения с разными знаками."""
        self.assertEqual(multiply(-2, 5), -10)
        self.assertEqual(multiply(2, -5), -10)
    
    def test_multiply_with_zero(self):
        """Тест умножения на ноль."""
        self.assertEqual(multiply(0, 100), 0)
        self.assertEqual(multiply(100, 0), 0)
        self.assertEqual(multiply(0, 0), 0)
    
    def test_multiply_with_one(self):
        """Тест умножения на единицу."""
        self.assertEqual(multiply(5, 1), 5)
        self.assertEqual(multiply(1, -5), -5)
    
    # ========== Тесты функции divide (деление) ==========
    
    def test_divide_positive_numbers(self):
        """Тест деления положительных чисел."""
        self.assertEqual(divide(10, 2), 5)
        self.assertEqual(divide(9, 3), 3)
        self.assertEqual(divide(100, 4), 25)
    
    def test_divide_negative_numbers(self):
        """Тест деления отрицательных чисел."""
        self.assertEqual(divide(-10, -2), 5)
        self.assertEqual(divide(-20, -5), 4)
    
    def test_divide_mixed_numbers(self):
        """Тест деления с разными знаками."""
        self.assertEqual(divide(-10, 2), -5)
        self.assertEqual(divide(10, -2), -5)
    
    def test_divide_float_result(self):
        """Тест деления с дробным результатом."""
        self.assertEqual(divide(7, 2), 3.5)
        self.assertEqual(divide(1, 4), 0.25)
        self.assertAlmostEqual(divide(1, 3), 0.3333333333333333, places=7)
    
    def test_divide_by_one(self):
        """Тест деления на единицу."""
        self.assertEqual(divide(10, 1), 10)
        self.assertEqual(divide(-5, 1), -5)
    
    def test_divide_by_zero(self):
        """Тест деления на ноль - должна вызываться ошибка ValueError."""
        with self.assertRaises(ValueError) as context:
            divide(10, 0)
        self.assertEqual(str(context.exception), "Деление на ноль невозможно!")
        
        # Проверка с отрицательным числом
        with self.assertRaises(ValueError):
            divide(-5, 0)
    
    # ========== Тесты функции power (возведение в степень) ==========
    
    def test_power_positive_exponent(self):
        """Тест возведения в положительную степень."""
        self.assertEqual(power(2, 3), 8)
        self.assertEqual(power(5, 2), 25)
        self.assertEqual(power(3, 4), 81)
    
    def test_power_zero_exponent(self):
        """Тест возведения в степень ноль (любое число в степени 0 = 1)."""
        self.assertEqual(power(10, 0), 1)
        self.assertEqual(power(-5, 0), 1)
        self.assertEqual(power(0, 0), 1)
    
    def test_power_one_exponent(self):
        """Тест возведения в степень 1 (число остается без изменений)."""
        self.assertEqual(power(5, 1), 5)
        self.assertEqual(power(-3, 1), -3)
    
    def test_power_negative_exponent(self):
        """Тест возведения в отрицательную степень (дробный результат)."""
        self.assertEqual(power(2, -1), 0.5)
        self.assertEqual(power(10, -1), 0.1)
        self.assertAlmostEqual(power(2, -2), 0.25, places=7)
    
    def test_power_fractional_base(self):
        """Тест возведения дробного числа в степень."""
        self.assertAlmostEqual(power(0.5, 2), 0.25, places=7)
        self.assertAlmostEqual(power(2.5, 2), 6.25, places=7)


if __name__ == '__main__':
    unittest.main()
