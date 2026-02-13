import os
from ebooklib import epub

def create_manga_epub(root_folder):
    # Создаем объект книги
    book = epub.EpubBook()

    # 1. Метаданные (Оглавление увидит это)
    #book.set_identifier('id123456')
    #book.set_title(root_folder)
    #book.set_language('ru')
    #book.add_author('Author Name')

    # Списки для наполнения оглавления (TOC) и спина (порядок чтения)
    epub_chapters = []
    toc_links = []
    spine = []

    # 2. Проходим по папкам-главам
    chapter_folders = [f for f in os.listdir(root_folder) 
                       if os.path.isdir(os.path.join(root_folder, f))]

    for ch_folder in chapter_folders:
        ch_path = os.path.join(root_folder, ch_folder)
        
        # Создаем HTML файл для главы
        file_name = f"{ch_folder}.xhtml"
        chapter = epub.EpubHtml(title=ch_folder, file_name=file_name)
        
        # Начало контента главы (CSS стиль для центрирования и ширины 100%)
        chapter.content = f'''
        <div style="text-align: center;">
        '''

        # 3. Проходим по картинкам внутри папки главы
        images = [f for f in os.listdir(ch_path) 
                  if f.lower().endswith(('.png', '.jpg', '.jpeg', '.webp'))]

        for img_name in images:
            img_full_path = os.path.join(ch_path, img_name)
            
            # Читаем картинку
            with open(img_full_path, 'rb') as f:
                img_content = f.read()

            # ВАЖНО: Чтобы избежать конфликтов имен (если в Главе 1 и Главе 2 есть файл "1.jpg"),
            # добавляем имя папки в имя файла внутри EPUB.
            internal_filename = f"images/{ch_folder}_{img_name}"
            
            # Определяем тип
            media_type = 'image/jpeg'
            if img_name.lower().endswith('.png'): media_type = 'image/png'
            elif img_name.lower().endswith('.webp'): media_type = 'image/webp'

            # Добавляем файл картинки в книгу
            img_item = epub.EpubItem(
                uid=internal_filename,
                file_name=internal_filename,
                media_type=media_type,
                content=img_content
            )
            book.add_item(img_item)

            # Добавляем тег <img> в HTML главы
            chapter.content += f'<img src="{internal_filename}" style="max-width: 100%; height: auto;" /><br/>'

        # Конец контента главы
        chapter.content += '</div>'

        # Добавляем главу в книгу
        book.add_item(chapter)
        
        # Добавляем в списки для структуры
        epub_chapters.append(chapter)
        toc_links.append(chapter)
        spine.append(chapter)

    # 4. Настройка Навигации (Оглавления)
    book.toc = tuple(toc_links)
    
    # Добавляем файлы навигации
    book.add_item(epub.EpubNcx())
    book.add_item(epub.EpubNav())

    # Устанавливаем порядок чтения (спин)
    book.spine = spine

    # 5. Запись файла на диск
    epub.write_epub(root_folder + ".epub", book, {})
    print("EPUB успешно создан")

# === ЗАПУСК ===
# Укажите путь к корневой папке и название результата
create_manga_epub("./Ryuu_to_Yuusha_to_Haitatsunin")