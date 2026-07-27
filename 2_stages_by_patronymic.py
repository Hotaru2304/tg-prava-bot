import random

def generate_random_pass():
    return f"{random.randint(1000, 9999)} {random.randint(100000, 999999)}"

print("Вставьте текст (после ввода нажмите Enter дважды для обработки):")

lines = []
while True:
    line = input()
    if line == "":
        break
    lines.append(line.strip())

if len(lines) >= 6:
    fio_1 = lines[0]
    date_1 = lines[1]
    pass_1 = lines[2]
    line_4 = lines[3]
    pass_2 = lines[4]
    date_2 = lines[5]

    # Имя из первой строки (Онищенко Эльвира Андреевна -> Эльвира)
    parts_1 = fio_1.split()
    name_1 = parts_1[1] if len(parts_1) > 1 else ""

    # Разбор 4-й строки (с проверкой на наличие числа в начале)
    parts_4 = line_4.split()
    if parts_4[0][0].isdigit(): # Если первый элемент начинается с цифры (0.46)
        prefix_4 = parts_4[0]
        surname_2 = parts_4[1]
        name_2 = parts_4[2]
        patronymic_2 = parts_4[3]
    else: # Если ввели сразу БАЧУРИНА СОФЬЯ АНДРЕЕВНА
        prefix_4 = "0.00" # Значение по умолчанию
        surname_2 = parts_4[0]
        name_2 = parts_4[1]
        patronymic_2 = parts_4[2]

    fio_2_full = f"{surname_2} {name_2} {patronymic_2}"
    rand_pass = generate_random_pass()

    print("\n--- ГОТОВЫЙ ТЕКСТ ---")
    # Блок 1
    print(f"{fio_1}")
    print(f"{date_1}")
    print(f"{pass_1}")
    print(f"{name_2.upper()} {name_1} {patronymic_2.upper()}")
    print(f"{rand_pass}")
    print(f"{date_2}")
    
    print()
    
    # Блок 2
    print(f"{prefix_4}: {fio_2_full.upper()}")
    print(f"{date_1}")
    print(f"{pass_2}")
    print(f"{name_1} {name_2.upper()} {patronymic_2.upper()}")
    print(f"{rand_pass}")
    print(f"{date_2}")
else:
    print("Ошибка: введите 6 строк текста!")
