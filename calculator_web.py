"""
Веб-версия калькулятора с использованием Streamlit.
Красивый интерфейс в стиле классического калькулятора с кнопками.
"""

import streamlit as st
from calculator import add, subtract, multiply, divide, power

# Настройка страницы
st.set_page_config(
    page_title="Калькулятор",
    page_icon="🧮",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# CSS для стилизации калькулятора
st.markdown("""
<style>
    .calculator-container {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 20px 30px 30px 30px;
        border-radius: 20px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.3);
        max-width: 500px;
        margin: 0 auto;
        margin-top: 0;
    }
    /* Скрываем стандартные элементы Streamlit над калькулятором */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stApp > header {
        display: none !important;
    }
    .display {
        background-color: #1e1e1e;
        color: #00ff00;
        padding: 20px;
        border-radius: 10px;
        font-size: 32px;
        text-align: right;
        font-family: 'Courier New', monospace;
        min-height: 80px;
        margin-bottom: 20px;
        border: 3px solid #333;
        word-wrap: break-word;
    }
    h1 {
        text-align: center !important;
        color: white !important;
        margin-bottom: 30px !important;
        margin-top: 0 !important;
        padding: 0 !important;
        font-size: 2.5rem !important;
    }
    .stButton > button {
        width: 100%;
        height: 60px;
        font-size: 24px;
        font-weight: bold;
        border-radius: 10px;
        transition: all 0.2s;
    }
    button[data-testid*="add"] {
        font-size: 28px !important;
        font-weight: bold !important;
    }
    button[data-testid*="subtract"] {
        font-size: 32px !important;
        font-weight: bold !important;
    }
</style>
""", unsafe_allow_html=True)

# Инициализация session state
if 'display' not in st.session_state:
    st.session_state.display = "0"
if 'current_number' not in st.session_state:
    st.session_state.current_number = "0"
if 'previous_number' not in st.session_state:
    st.session_state.previous_number = None
if 'operation' not in st.session_state:
    st.session_state.operation = None
if 'waiting_for_number' not in st.session_state:
    st.session_state.waiting_for_number = False

def input_number(num):
    """Обработка ввода цифры."""
    if st.session_state.waiting_for_number:
        st.session_state.current_number = num
        st.session_state.waiting_for_number = False
    elif st.session_state.current_number == "0":
        st.session_state.current_number = num
    else:
        st.session_state.current_number += num
    st.session_state.display = st.session_state.current_number

def input_decimal():
    """Обработка ввода десятичной точки."""
    if st.session_state.waiting_for_number:
        st.session_state.current_number = "0."
        st.session_state.waiting_for_number = False
    elif "." not in st.session_state.current_number:
        st.session_state.current_number += "."
    st.session_state.display = st.session_state.current_number

def clear_all():
    """Очищает все значения."""
    st.session_state.display = "0"
    st.session_state.current_number = "0"
    st.session_state.previous_number = None
    st.session_state.operation = None
    st.session_state.waiting_for_number = False

def backspace():
    """Удаляет последнюю цифру."""
    if st.session_state.waiting_for_number:
        return
    if len(st.session_state.current_number) > 1:
        st.session_state.current_number = st.session_state.current_number[:-1]
    else:
        st.session_state.current_number = "0"
    st.session_state.display = st.session_state.current_number

def negate():
    """Изменяет знак числа."""
    if st.session_state.waiting_for_number:
        return
    if st.session_state.current_number != "0":
        if st.session_state.current_number.startswith("-"):
            st.session_state.current_number = st.session_state.current_number[1:]
        else:
            st.session_state.current_number = "-" + st.session_state.current_number
        st.session_state.display = st.session_state.current_number

def set_operation(op):
    """Устанавливает операцию для вычисления."""
    if st.session_state.operation is not None and st.session_state.previous_number is not None:
        # Выполняем предыдущую операцию перед установкой новой
        calculate_result()
    
    st.session_state.previous_number = float(st.session_state.current_number)
    st.session_state.operation = op
    st.session_state.waiting_for_number = True

def calculate_result():
    """Выполняет вычисление."""
    if st.session_state.operation is None or st.session_state.previous_number is None:
        return
    
    try:
        num1 = st.session_state.previous_number
        num2 = float(st.session_state.current_number)
        
        if st.session_state.operation == '+':
            result = add(num1, num2)
        elif st.session_state.operation == '-':
            result = subtract(num1, num2)
        elif st.session_state.operation == '*':
            result = multiply(num1, num2)
        elif st.session_state.operation == '/':
            result = divide(num1, num2)
        elif st.session_state.operation == '^':
            result = power(num1, num2)
        else:
            return
        
        # Форматируем результат
        if result == int(result):
            result_str = str(int(result))
        else:
            result_str = str(result)
        
        st.session_state.display = result_str
        st.session_state.current_number = result_str
        st.session_state.previous_number = None
        st.session_state.operation = None
        st.session_state.waiting_for_number = False
        
    except ValueError as e:
        st.session_state.display = "Ошибка!"
        st.error(f"❌ {e}")
        clear_all()
    except Exception as e:
        st.session_state.display = "Ошибка!"
        st.error(f"❌ Произошла ошибка: {e}")
        clear_all()

# Основной интерфейс калькулятора
st.markdown('<div class="calculator-container">', unsafe_allow_html=True)

# Заголовок с правильным выравниванием
st.markdown("""
<div style="text-align: center; color: white; margin-bottom: 30px; margin-top: 0; padding: 0; font-size: 2.5rem; font-weight: bold; width: 100%;">
🧮 Калькулятор
</div>
""", unsafe_allow_html=True)

# Дисплей калькулятора
st.markdown(f'<div class="display">{st.session_state.display}</div>', unsafe_allow_html=True)

# Обработка нажатий кнопок
# Первая строка: C, ⌫, ^, /
col1, col2, col3, col4 = st.columns(4)
with col1:
    if st.button("C", key="clear", use_container_width=True, type="primary"):
        clear_all()
        st.rerun()
with col2:
    if st.button("⌫", key="backspace", use_container_width=True):
        backspace()
        st.rerun()
with col3:
    if st.button("^", key="power", use_container_width=True):
        set_operation('^')
        st.rerun()
with col4:
    if st.button("/", key="divide", use_container_width=True):
        set_operation('/')
        st.rerun()

# Вторая строка: 7, 8, 9, *
col1, col2, col3, col4 = st.columns(4)
with col1:
    if st.button("7", key="7", use_container_width=True):
        input_number("7")
        st.rerun()
with col2:
    if st.button("8", key="8", use_container_width=True):
        input_number("8")
        st.rerun()
with col3:
    if st.button("9", key="9", use_container_width=True):
        input_number("9")
        st.rerun()
with col4:
    if st.button("×", key="multiply", use_container_width=True):
        set_operation('*')
        st.rerun()

# Третья строка: 4, 5, 6, -
col1, col2, col3, col4 = st.columns(4)
with col1:
    if st.button("4", key="4", use_container_width=True):
        input_number("4")
        st.rerun()
with col2:
    if st.button("5", key="5", use_container_width=True):
        input_number("5")
        st.rerun()
with col3:
    if st.button("6", key="6", use_container_width=True):
        input_number("6")
        st.rerun()
with col4:
    if st.button("−", key="subtract", use_container_width=True):
        set_operation('-')
        st.rerun()

# Четвертая строка: 1, 2, 3, +
col1, col2, col3, col4 = st.columns(4)
with col1:
    if st.button("1", key="1", use_container_width=True):
        input_number("1")
        st.rerun()
with col2:
    if st.button("2", key="2", use_container_width=True):
        input_number("2")
        st.rerun()
with col3:
    if st.button("3", key="3", use_container_width=True):
        input_number("3")
        st.rerun()
with col4:
    if st.button("➕", key="add", use_container_width=True):
        set_operation('+')
        st.rerun()

# Пятая строка: 0, ., =, ±
col1, col2, col3, col4 = st.columns(4)
with col1:
    if st.button("0", key="0", use_container_width=True):
        input_number("0")
        st.rerun()
with col2:
    if st.button(".", key="decimal", use_container_width=True):
        input_decimal()
        st.rerun()
with col3:
    if st.button("=", key="equals", use_container_width=True, type="primary"):
        calculate_result()
        st.rerun()
with col4:
    if st.button("±", key="negate", use_container_width=True):
        negate()
        st.rerun()

st.markdown('</div>', unsafe_allow_html=True)

# Информационная панель внизу
st.markdown("---")
with st.expander("ℹ️ Справка"):
    st.markdown("""
    **Как пользоваться:**
    - Нажмите на цифры для ввода числа
    - Выберите операцию (+, -, ×, /, ^)
    - Нажмите "=" для вычисления результата
    - Нажмите "C" для очистки
    - Нажмите "⌫" для удаления последней цифры
    - Нажмите "±" для изменения знака числа
    
    **Доступные операции:**
    - ➕ Сложение
    - ➖ Вычитание  
    - ✖️ Умножение
    - ➗ Деление
    - 🔢 Возведение в степень
    """)
