import math
import locale
import os
from datetime import datetime as dt

def show_log(log):
    if log:
        for k, i in log.items():
            print(f"{k}   {i}")
    else:
        print(f"В текущую сессию пользователь не выполнял операций")

def save_history_to_file(history, fn="calc_console_log.txt"):
    # файл сохраняется рядом с файлом приложения
    fn = os.path.join(os.path.dirname(os.path.abspath(__file__)), fn)

    try:
        with open(fn, "a", encoding="utf-8") as f:
            if history:
                for key, value in history.items():
                    f.write(f"{key}   {value}\n")
            else:
                f.write("В текущую сессию пользователь не выполнял операций\n")
    except OSError as e:
        print(f"Не удалось сохранить историю в файл: {e}")

def dec_separator(a):
    if isinstance(a, (int, float)):
        return(a)

    locale.setlocale(locale.LC_ALL, "")
    locale_info = locale.localeconv()
    dec_p = locale_info["decimal_point"]

    if dec_p == '.':
        a = a.replace(',',dec_p)
            
    else:    
        a = a.replace('.', dec_p)
    return locale.atof(a) 

def only_operator(a, history = None):
    r_chars=('+', '/', '*', '-', 'log', 'sin')
    w_text = a.strip()
    if w_text.lower() == 'q' or w_text.lower() == 'й':
        return 'q'
    if w_text.lower() == 'h' or w_text.lower() == 'р':
        show_log(history)

    if w_text in r_chars:
        return w_text

    print("Допустимы только '+', '/', '*', '-', 'log'")


def only_num(input_t, history = None):

    w_text = input_t.strip()

    if w_text.lower() == 'q' or w_text.lower() == 'й':
        return 'q'
    if w_text.lower() == 'h' or w_text.lower() == 'р':
        show_log(history)
        return 'h'
        

    r_text = w_text.strip('-')

    if r_text and (r_text.count('.') + r_text.count(',') <=1) and all(c.isdigit() or c in ',.' for c in r_text):
        return w_text

    print('Допустимы только цифры точка и запятая')


def is_finite_number(x):
    """Проверяет, что значение — конечное число (не inf и не nan)."""
    return isinstance(x, (int, float)) and math.isfinite(x)





# Список операций для меню: (номер, название, символ оператора)
OPERATIONS = {
    '1': ('Сложение', '+'),
    '2': ('Вычитание', '-'),
    '3': ('Умножение', '*'),
    '4': ('Деление', '/'),
    '5': ('Логарифм', 'log'),
    '6': ('Синус (угол в радианах)', 'sin'),
}

# Операции, требующие только одного аргумента
UNARY_OPERATIONS = ('sin',)


def show_menu():
    print('''
Калькулятор с простыми арифметическими действиями и вычислением логарифма
##########################################################################
                    ВЫБЕРИТЕ ОПЕРАЦИЮ:''')
    for num, (name, op) in OPERATIONS.items():
        print(f"  {num}. {name} ({op})")
    print('''  h. История операций
  q. Выход''')


def choose_operation():
    """Возвращает символ оператора либо 'h' / 'q'."""
    while True:
        choice = input('Ваш выбор: ').strip().lower()
        if choice == 'q' or choice == 'й':
            return 'q'
        if choice == 'h' or choice == 'р':
            return 'h'
        if choice in OPERATIONS:
            return OPERATIONS[choice][1]
        print('Неверный пункт меню, попробуйте ещё раз')


def input_number(prompt, history):
    """Запрашивает число, возвращает float либо 'h' / 'q'."""
    while True:
        a = only_num(input(prompt), history)
        if a in ('q', 'h'):
            return a
        if a is None:
            continue
        num = dec_separator(a)
        if not is_finite_number(num):
            print('Слишком большое или некорректное число, повторите ввод')
            continue
        return num


def calculate(o, aa, bb):
    """Выполняет выбранную операцию. Возвращает результат либо None при ошибке."""
    if o == '+':
        return aa + bb
    if o == '-':
        return aa - bb
    if o == '*':
        return aa * bb
    if o == '/':
        if bb == 0:
            print('На 0 делить нельзя')
            return None
        return aa / bb
    if o == 'log':
        if bb < 0 or bb == 1:
            print('''Основание логарифма не может быть отрицательным
            или равняться единице''')
            return None
        if aa <= 0:
            print('Аргумент логарифма должен быть положительным')
            return None
        return math.log(aa, bb)
    if o == 'sin':
        if not is_finite_number(aa):
            print('Угол должен быть конечным числом')
            return None
        if abs(aa) > 1e9:
            print('Угол слишком велик по модулю (максимум 1e9 радиан), '
                  'большой аргумент приводит к потере точности')
            return None
        return math.sin(aa)


history = {}
while True:
    show_menu()
    o = choose_operation()

    if o == 'q':
        print('Программа завершена')
        break
    if o == 'h':
        show_log(history)
        continue

    if o in UNARY_OPERATIONS:
        a = input_number('Введите угол в радианах: ', history)
        if a == 'q':
            print('Программа завершена')
            break
        if a == 'h':
            show_log(history)
            continue
        b = None
    else:
        a = input_number('Введите первое число (аргумент логарифма): ', history)
        if a == 'q':
            print('Программа завершена')
            break
        if a == 'h':
            show_log(history)
            continue

        b = input_number('Введите второе число (основание логарифма): ', history)
        if b == 'q':
            print('Программа завершена')
            break
        if b == 'h':
            show_log(history)
            continue

    c = calculate(o, a, b)
    if c is None:
        continue

    key_time = dt.now().strftime("%d-%m-%Y %H:%M:%S")
    if o in UNARY_OPERATIONS:
        expression = f"{o}({a})"
    else:
        expression = f"{a} {o} {b}"
    history[key_time] = f"{expression} = {c}"

    print(f"Результат: {expression} = {c}\n")

# история сохраняется перед закрытием программы
save_history_to_file(history)
