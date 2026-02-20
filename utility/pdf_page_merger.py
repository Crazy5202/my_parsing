from pypdf import PdfReader, PdfWriter
import glob
import os

# Настройки
# Обратите внимание на букву 'r' перед строкой пути — это важно для Windows
path = r"G:\Мои документы\транснефть_2026\Документы_отправка\Личные_данные\\"
output_filename = "result_selected_pages.pdf"

# Список номеров страниц, которые нужно извлечь (нумерация с 0).
# Например: [0] - только 1-я страница, [0, 2] - 1-я и 3-я, [-1] - последняя страница.
pages_to_extract = [[3], [2], [0]] 

writer = PdfWriter()

# Получаем список всех PDF файлов и сортируем их по времени изменения
all_pdfs = sorted(glob.glob(path + "*.pdf"), key=os.path.getmtime)

# Если хотите обрабатывать только последние N файлов (как было в заготовке), раскомментируйте строку ниже:
# num = 3
# all_pdfs = all_pdfs[-num:]
counter = 0

for file_path in all_pdfs:
    # Пропускаем файл результата, если он уже лежит в папке, чтобы не добавить его сам в себя
    if os.path.basename(file_path) == output_filename:
        continue
    
    try:
        # Открываем текущий PDF для чтения
        reader = PdfReader(file_path)
        file_name = os.path.basename(file_path)
        
        print(f"Обработка файла: {file_name} (всего страниц: {len(reader.pages)})")

        for page_num in pages_to_extract[counter]:
            # Проверка, что страница существует в документе
            # (нужна, например, при выборе последней страницы [-1] в пустом файле)
            if abs(page_num) <= len(reader.pages):
                # Добавляем выбранную страницу в общий писатель
                writer.add_page(reader.pages[page_num])
                print(f"  -> Добавлена страница №{page_num + 1}")
            else:
                print(f"  -> Страница №{page_num} не найдена в файле")
        counter += 1

    except Exception as e:
        print(f"Ошибка при чтении файла {file_path}: {e}")

# Сохраняем все собранные страницы в один файл
full_output_path = path + output_filename
with open(full_output_path, "wb") as output_file:
    writer.write(output_file)

print(f"\nГотово! Итоговый файл сохранен: {full_output_path}")