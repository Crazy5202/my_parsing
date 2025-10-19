from pypdf import PdfReader, PdfWriter
import os

def extract_page_range(input_pdf, output_pdf, start_page, end_page):
    """
    Вырезает диапазон страниц
    """
    reader = PdfReader(input_pdf)
    writer = PdfWriter()
    
    for page_num in range(start_page-1, end_page):
        if page_num < len(reader.pages):
            writer.add_page(reader.pages[page_num])
    
    with open(output_pdf, 'wb') as output_file:
        writer.write(output_file)

input_path = str(input("Введите путь к файлу: "))
a = int(input("Левая граница: "))
b = int(input("Левая граница: "))
output_path = os.path.join(os.path.dirname(input_path), 'output.pdf')

extract_page_range(input_path, output_path, a, b)