import os
import webbrowser
import time
import pyautogui
import pyperclip
from datetime import datetime

# Настройки задержек для идеальной точности
pyautogui.PAUSE = 0.4  
pyautogui.FAILSAFE = True  

script_dir = os.path.dirname(os.path.abspath(__file__))
path_data_txt = os.path.join(script_dir, 'data.txt')

url = "https://b2c.astrovolga.ru/personal/index.php?login=yes"

def paste_via_buffer(text):
    """Вставка текста через буфер обмена"""
    if not text:
        return
    pyperclip.copy(str(text))
    time.sleep(0.1)
    pyautogui.hotkey('ctrl', 'v')
    time.sleep(0.2)

def type_date_manually(date_str):
    """Посимвольный ввод цифр даты (маска сайта сама ставит точки)"""
    if not date_str:
        return
    for char in date_str:
        pyautogui.press(char)
        time.sleep(0.05)
    time.sleep(0.2)

def fill_single_driver(lines_block, driver_number):
    """Универсальная функция заполнения одного блока водителя"""
    print(f"\n--- ЗАПОЛНЯЮ ВОДИТЕЛЯ №{driver_number} ---")
    
    txt_new_fam   = lines_block[0]
    txt_new_name  = lines_block[1]
    txt_new_otch  = lines_block[2]
    txt_birth_str = lines_block[3]
    txt_new_seria = lines_block[4]
    txt_new_nomer = lines_block[5]
    txt_old_fam   = lines_block[6]
    txt_old_seria = lines_block[7]
    txt_old_nomer = lines_block[8]

    str_birth = txt_birth_str.replace('.', '')
    try:
        if '.' in txt_birth_str:
            birth_date = datetime.strptime(txt_birth_str, "%d.%m.%Y")
        else:
            birth_date = datetime.strptime(txt_birth_str, "%d%m%Y")
            
        # Стаж всегда начинается в 18 лет
        stazh_start_date = birth_date.replace(year=birth_date.year + 18)
        old_issue_date = stazh_start_date
        
        # Вычисляем год последнего теоретического обновления прав
        today = datetime.now()
        years_since_stazh = today.year - stazh_start_date.year
        cycles = years_since_stazh // 10
        last_issue_year = stazh_start_date.year + (cycles * 10)
        
        # Создаем предварительную дату выдачи новых прав
        new_issue_date = stazh_start_date.replace(year=last_issue_year)
        
        # Если рассчитанная дата обгоняет сегодняшний день, откатываемся на 10 лет назад
        if new_issue_date > today:
            new_issue_date = new_issue_date.replace(year=new_issue_date.year - 10)

        str_birth = birth_date.strftime("%d%m%Y")
        str_stazh_start = stazh_start_date.strftime("%d%m%Y")
        str_old_issue = old_issue_date.strftime("%d%m%Y")
        str_new_issue = new_issue_date.strftime("%d%m%Y")
    except Exception:
        str_birth = txt_birth_str.replace('.', '')
        str_stazh_start = "03092006"
        str_old_issue = "03092006"
        str_new_issue = "03092016"


    # 1. Поле: Фамилия
    print(f"Ввожу фамилию: {txt_new_fam}")
    paste_via_buffer(txt_new_fam)

    # 2. Поле: Имя
    pyautogui.press('tab')
    time.sleep(0.15)
    print(f"Ввожу имя: {txt_new_name}")
    paste_via_buffer(txt_new_name)

    # 3. Поле: Отчество
    pyautogui.press('tab')
    time.sleep(0.15)
    
    if txt_new_otch.lower() in ['-', '', 'нет', 'отсутствует']:
        pyautogui.press('tab') 
        time.sleep(0.1)
        pyautogui.press('space') 
        time.sleep(0.2)
        pyautogui.press('tab') 
    else:
        print(f"Ввожу отчество: {txt_new_otch}")
        paste_via_buffer(txt_new_otch)
        pyautogui.press('tab')
        time.sleep(0.1)
        pyautogui.press('tab')

    # 4. Поле: Дата рождения
    time.sleep(0.2)
    print(f"Печатаю дату рождения: {str_birth}")
    type_date_manually(str_birth)

    # 5. Поле: Серия нового ВУ
    pyautogui.press('tab') 
    time.sleep(0.1)
    pyautogui.press('tab') 
    time.sleep(0.15)
    print(f"Ввожу серию нового ВУ: {txt_new_seria}")
    paste_via_buffer(txt_new_seria)

    # 6. Поле: Номер нового ВУ
    pyautogui.press('tab')
    time.sleep(0.15)
    print(f"Ввожу номер нового ВУ: {txt_new_nomer}")
    paste_via_buffer(txt_new_nomer)

    # 7. Поле: Дата начала стажа
    pyautogui.press('tab')
    time.sleep(0.2)
    print(f"Печатаю дату начала стажа: {str_stazh_start}")
    type_date_manually(str_stazh_start)
    time.sleep(0.5) 

    # 8. Поле: Дата выдачи новых ВУ
    pyautogui.press('tab') 
    time.sleep(0.3)
    print(f"Печатаю дату выдачи новых ВУ: {str_new_issue}")
    type_date_manually(str_new_issue)
    time.sleep(0.4)

    # Переход к блоку старых прав
    pyautogui.press('tab') 
    time.sleep(0.2)
    pyautogui.press('tab') 
    time.sleep(0.2)
    pyautogui.press('tab') 
    time.sleep(0.4)

    # 9. Блок старых данных
    print(f"Ввожу серию старого ВУ: {txt_old_seria}")
    paste_via_buffer(txt_old_seria)
    time.sleep(0.2)
    
    pyautogui.press('tab')
    time.sleep(0.2)
    print(f"Ввожу номер старого ВУ: {txt_old_nomer}")
    paste_via_buffer(txt_old_nomer)
    time.sleep(0.2)
    
    pyautogui.press('tab')
    time.sleep(0.1)
    print(f"Печатаю дату выдачи старого ВУ: {str_old_issue}")
    type_date_manually(str_old_issue)
    time.sleep(0.3)
    
    pyautogui.press('tab')
    time.sleep(0.1)
    pyautogui.press('tab')
    time.sleep(0.1)
    print(f"Ввожу старую фамилию: {txt_old_fam}")
    paste_via_buffer(txt_old_fam)

def fill_all_data():
    if not os.path.exists(path_data_txt):
        print("❌ Файл data.txt не найден!")
        return

    with open(path_data_txt, 'r', encoding='utf-8') as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    total_lines = len(lines)
    total_drivers = total_lines // 9

    if total_drivers == 0:
        print("❌ Ошибка: В файле data.txt недостаточно строк. Нужно минимум 9 строк на одного водителя!")
        return

    print(f"📊 Обнаружено водителей в файле data.txt: {total_drivers}")
    
    # ВОЗВРАТ К СТАРОЙ ИНСТРУКЦИИ С ENTER
    print("\n=== ИНСТРУКЦИЯ ===")
    print("1. Нажмите на сайте 'Добавить водителя' столько раз, сколько людей записано в data.txt.")
    print("2. Проставьте все нужные чекбоксы на формах.")
    print("3. Вручную поставьте курсор в поле 'Фамилия' ПЕРВОГО нового водителя.")
    print("4. Вернитесь сюда и нажмите Enter для запуска заполнения.")
    
    input("\nНажмите Enter, когда будете готовы: ")
    
    print("\n🚀 Поехали! Начинаю автоматическое заполнение...\n")
    pyautogui.click()  # Подтверждающий клик по полю ввода
    time.sleep(0.3)

    for current_index in range(total_drivers):
        start_line = current_index * 9
        end_line = start_line + 9
        driver_block = lines[start_line:end_line]
        driver_num = current_index + 1

        # Заполняем текущего водителя
        fill_single_driver(driver_block, driver_num)
        
        # Переход к следующей готовой форме по Tab
        if driver_num < total_drivers:
            print(f"\nПерепрыгиваю на форму водителя №{driver_num + 1}...")
            for _ in range(3):
                pyautogui.press('tab')
                time.sleep(0.08)
            time.sleep(0.3)

    print(f"\n🎉 [УСПЕХ] Все водители ({total_drivers} шт.) из файла успешно заполнены!")

if __name__ == "__main__":
    print("Открываю ссылку...")
    webbrowser.open_new_tab(url)
    time.sleep(1.5)  
    
    fill_all_data()
