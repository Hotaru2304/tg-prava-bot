import os
import re

# Путь к файлу данных
script_dir = os.path.dirname(os.path.abspath(__file__))
path_data_txt = os.path.join(script_dir, 'data.txt')

def parse_and_save_driver(raw_text):
    # Разбираем текст на строки и убираем лишние пробелы
    lines = [line.strip() for line in raw_text.strip().split('\n') if line.strip()]
    
    if len(lines) < 5:
        print("❌ Ошибка: Вставленный текст слишком короткий!")
        return False

    try:
        # 1. Первая строчка (Новые ФИО)
        fio_new_line = re.sub(r'^[0-9.:\s]+', '', lines[0]).strip()
        fio_new_words = fio_new_line.split()
        
        new_fam = fio_new_words[0].capitalize()
        new_name = fio_new_words[1].capitalize() if len(fio_new_words) > 1 else "Нет"
        new_otch = fio_new_words[2].capitalize() if len(fio_new_words) > 2 else "Нет"

        # 2. Вторая строчка (Дата рождения)
        birth_date = lines[1].strip()

        # 3. Третья строчка (Новые права: серия и номер)
        rights_new = lines[2].split()
        new_seria = rights_new[0].upper() if len(rights_new) > 0 else "0000"
        new_nomer = rights_new[1] if len(rights_new) > 1 else "000000"

        # 4. Четвертая строчка (Старые ФИО -> берем первое слово как Старую фамилию)
        fio_old_line = re.sub(r'^[0-9.:\s]+', '', lines[3]).strip()
        fio_old_words = fio_old_line.split()
        old_fam = fio_old_words[0].capitalize() if fio_old_words else "Нет"

        # 5. Пятая строчка (Старые права: серия и номер)
        rights_old = lines[4].split()
        old_seria = rights_old[0].upper() if len(rights_old) > 0 else "0000"
        old_nomer = rights_old[1] if len(rights_old) > 1 else "000000"

        # Собираем блок из 9 строк
        driver_block = [
            new_fam, new_name, new_otch,
            birth_date,
            new_seria, new_nomer,
            old_fam,
            old_seria, old_nomer
        ]

        # Гарантируем, что запись начнется с новой строки, если файл не пустой
        need_newline = False
        if os.path.exists(path_data_txt) and os.path.getsize(path_data_txt) > 0:
            with open(path_data_txt, 'r', encoding='utf-8') as f:
                # Если последний символ в файле не перенос строки, добавим его
                f.seek(0, os.SEEK_END)
                f.seek(f.tell() - 1, os.SEEK_SET)
                if f.read(1) != '\n':
                    need_newline = True

        # Записываем данные в data.txt
        with open(path_data_txt, 'a', encoding='utf-8') as f:
            if need_newline:
                f.write('\n')
            for item in driver_block:
                f.write(f"{item}\n")
                
        print(f"✅ Водитель {new_fam} {new_name} успешно добавлен строго с новой строки!")
        return True

    except Exception as e:
        print(f"❌ Произошла ошибка при разборе текста: {e}")
        return False

if __name__ == "__main__":
    print("=== АВТОМАТИЧЕСКИЙ КОНВЕРТЕР ДАННЫХ ДЛЯ АСТРЫ ===")
    print("Вставьте текст водителя. Для окончания ввода ОСТАВЬТЕ СТРОКУ ПУСТОЙ и нажмите Enter:")
    
    input_lines = []
    while True:
        line = input()
        # Если строка пустая — прекращаем считывание
        if line.strip() == "":
            break
        input_lines.append(line)
            
    raw_input_text = "\n".join(input_lines)
    
    if raw_input_text.strip():
        parse_and_save_driver(raw_input_text)
    else:
        print("❌ Вы ничего не ввели.")
