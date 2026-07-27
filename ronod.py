from datetime import datetime, timedelta

def generate_dates():
    start_str = input("Введите начальную дату (ДД.ММ.ГГГГ): ").strip()
    end_str = input("Введите конечную дату (ДД.ММ.ГГГГ): ").strip()

    try:
        current_date = datetime.strptime(start_str, "%d.%m.%Y")
        end_date = datetime.strptime(end_str, "%d.%m.%Y")
    except ValueError:
        print("Ошибка: используйте формат ДД.ММ.ГГГГ")
        return

    patronymics = [
        ";;Сергеевич", ";;Александрович", ";;Алексеевич", 
        ";;Владимирович", ";;Андреевич"
    ]

    while current_date <= end_date:
        date_display = current_date.strftime("%d.%m.%Y")
        
        # Печатаем блок отчеств для текущего дня
        for pat in patronymics:
            print(f"{pat} {date_display}")
        
        next_date = current_date + timedelta(days=1)
        
        # Проверка на переход месяца
        if next_date.month != current_date.month and next_date <= end_date:
            print("\n") # Два переноса строки (те самые 2 пробела между блоками)
            
        current_date = next_date

if __name__ == "__main__":
    generate_dates()
