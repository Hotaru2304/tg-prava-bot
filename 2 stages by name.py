import random

def generate_random_pass():
    return f"{random.randint(1000, 9999)} {random.randint(100000, 999999)}"

def clean_line(text):
    return " ".join(text.split()).strip()

def transform_data():
    print("Вставьте 6 строк данных и нажмите Enter дважды:")
    lines = []
    while True:
        try:
            line = input()
            if not line and len(lines) >= 6: break
            if not line and len(lines) == 0: continue
            lines.append(line)
        except EOFError:
            break

    if len(lines) < 6:
        print("Ошибка: Введено меньше 6 строк.")
        return

    # Чтение исходных данных
    fio1 = clean_line(lines[0])
    dob1 = clean_line(lines[1])
    pass1 = clean_line(lines[2])
    line4_raw = clean_line(lines[3])
    pass2 = clean_line(lines[4])
    dob2 = clean_line(lines[5])

    # Разбор 4-й строки (0.52: ЕФРЕМОВ МИХАИЛ ВИТАЛЬЕВИЧ)
    if ":" in line4_raw:
        coef_part, fio2_raw = line4_raw.split(":", 1)
        coef = coef_part.strip()
        fio2 = clean_line(fio2_raw)
    else:
        coef, fio2 = "0.52", clean_line(line4_raw)

    # Разбивка ФИО на части
    p1 = fio1.split() # Гуцаев Михаил Тариелович
    p2 = fio2.split() # ЕФРЕМОВ МИХАИЛ ВИТАЛЬЕВИЧ

    # Части первого ФИО (индексы: 0-Фамилия, 1-Имя, 2-Отчество)
    p1_i = p1[1] if len(p1) > 1 else ""
    p1_o = p1[2] if len(p1) > 2 else ""

    # Части второго ФИО (делаем их КАПСОМ для соответствия примеру)
    p2_i = p2[1].upper() if len(p2) > 1 else ""
    p2_o = p2[2].upper() if len(p2) > 2 else ""

    rand_pass = generate_random_pass()

    # Формирование итогового текста строго по примеру
    print("\n--- РЕЗУЛЬТАТ ---")
    
    # Блок 1
    print(f"{fio1}")
    print(f"{dob1}")
    print(f"{pass1}")
    # ВИТАЛЬЕВИЧ МИХАИЛ Тариелович
    print(f"{p2_o} {p2_i} {p1_o}")
    print(f"{rand_pass}")
    print(f"{dob2}")

    print() # Пустая строка

    # Блок 2
    print(f"{coef}: {fio2.upper()}") # 0.52: ЕФРЕМОВ МИХАИЛ ВИТАЛЬЕВИЧ
    print(f"{dob1}")
    print(f"{pass2}")
    # Тариелович МИХАИЛ ВИТАЛЬЕВИЧ
    print(f"{p1_o} {p2_i} {p2_o}")
    print(f"{rand_pass}")
    print(f"{dob2}")

if __name__ == "__main__":
    transform_data()
