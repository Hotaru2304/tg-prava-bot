import random

def generate_random_pass():
    return f"{random.randint(1000, 9999)} {random.randint(100000, 999999)}"

def clean_s(text):
    return " ".join(text.split()).strip()

def transform_data():
    print("Вставьте данные (6 строк) и нажмите Enter дважды:")
    lines = []
    while True:
        line = input()
        if not line: break
        lines.append(line.strip())

    if len(lines) < 6:
        print("Ошибка: Нужно ввести 6 строк данных.")
        return

    fio1 = clean_s(lines[0])
    dob1 = lines[1]
    pass1 = clean_s(lines[2])
    
    line4_raw = lines[3]
    if ":" in line4_raw:
        prefix, fio2_raw = line4_raw.split(":", 1)
        prefix = prefix.strip() + ":"
        fio2 = clean_s(fio2_raw)
    else:
        prefix, fio2 = "", clean_s(line4_raw)
        
    pass2_orig = clean_s(lines[4])
    dob2 = lines[5]

    p1 = fio1.split()
    p2 = fio2.split()

    p1_n, p1_o = p1[1] if len(p1)>1 else "", p1[2] if len(p1)>2 else ""
    p2_n, p2_o = p2[1] if len(p2)>1 else "", p2[2] if len(p2)>2 else ""

    rand_a = generate_random_pass()
    rand_b = generate_random_pass()

    output = [
        f"{fio1}",
        f"{dob1}",
        f"{pass1}",
        clean_s(f"{p2_n} {p1_n} {p1_o}"),
        f"{rand_a}",
        f"{dob2}",
        "",
        clean_s(f"{p1_n} {p2_n} {p1_o}"),
        f"{dob1}",
        f"{rand_a}",
        clean_s(f"{p2_o} {p2_n} {p1_o}"),
        f"{rand_b}",
        f"{dob2}",
        "",
        clean_s(f"{p1_o} {p2_n} {p2_o}"),
        f"{dob1}",
        f"{rand_b}",
        f"{prefix} {fio2}".strip(),
        f"{pass2_orig}",
        f"{dob2}"
    ]

    print("\n--- РЕЗУЛЬТАТ ---")
    print("\n".join(output))

if __name__ == "__main__":
    transform_data()
