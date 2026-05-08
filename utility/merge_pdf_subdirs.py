from pypdf import PdfWriter
from PIL import Image
import glob
import os

path = "K:/Сети"
image = True

if image:
    subdirs = os.listdir(path)

    counter = 1

    for subdir in subdirs:
        full_dir_path = os.path.join(path, subdir)

        all_imgs = sorted(glob.glob(os.path.join(full_dir_path, "*.jpg")), key=os.path.getmtime)

        merger = PdfWriter()

        inner_counter = 0

        for image_file in all_imgs:

            img = Image.open(image_file)

            if img.mode != 'RGB':
                img = img.convert('RGB')

            temp_pdf_path = os.path.join(full_dir_path, f"temp_{inner_counter}.pdf")

            img.save(temp_pdf_path, "PDF", resolution=100.0)

            merger.append(temp_pdf_path)

            inner_counter += 1
        
        merger.write(os.path.join(path, f"Лекция_{counter}.pdf"))
        merger.close()

        counter += 1