from pypdf import PdfWriter
import glob
import os

path = "G:/Мои документы/Отсканированные документы/Обновлённое/М/"
num = 4

pdfs = []

all_pdfs = sorted(glob.glob(path+"*.pdf"), key=os.path.getmtime)

for file in all_pdfs[-num:]:
    pdfs.append(file)

merger = PdfWriter()

for pdf in pdfs:
    merger.append(pdf)

merger.write(path+"merged.pdf")
merger.close()