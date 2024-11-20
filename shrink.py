from PIL import Image
import os

input_dir = '.' # папка, в которой находятся изображения
output_dir = './compressed' # папка, в которую сохраняются изображения

os.makedirs(output_dir, exist_ok=True)

# целевые разрешение и размер в КБ
target_resolution = (1500, 1000)
max_file_size_kb = 500

def resize_and_compress_image(input_path, output_path): # функция сжатия отдельного изображения
    with Image.open(input_path) as img:
        img = img.resize(target_resolution, Image.LANCZOS)
        
        quality = 85

        while True:
            img.save(output_path, format='JPEG', quality=quality)
            if os.path.getsize(output_path) / 1024 <= max_file_size_kb or quality <= 10:
                break
            quality -= 5

for filename in os.listdir(input_dir): # обработка всех изображений
    if filename.lower().endswith(('.jpg', '.jpeg', '.png')):
        input_path = os.path.join(input_dir, filename)
        output_path = os.path.join(output_dir, filename)
        resize_and_compress_image(input_path, output_path)

print("Все изображения обработаны.")