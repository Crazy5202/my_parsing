from pypdf import PdfWriter
from PIL import Image
import glob
import os

path = "C:/Users/Maxim/Downloads/Telegram Desktop/"
num = 2
image = True

if image:
    all_imgs = sorted(glob.glob(path+"*.jpg"), key=os.path.getmtime)

    counter = 0

    for image_file in all_imgs[-num:]:
        img = Image.open(image_file)

        if img.mode != 'RGB':
            img = img.convert('RGB')

        temp_pdf_path = path+ f"temp_{counter}.pdf"

        img.save(temp_pdf_path, "PDF", resolution=100.0)

        counter += 1

all_pdfs = sorted(glob.glob(path+"*.pdf"), key=os.path.getmtime)

merger = PdfWriter()

for file in all_pdfs[-num:]:
    merger.append(file)

merger.write(path+"merged.pdf")
merger.close()