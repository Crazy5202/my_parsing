from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from random import uniform
from selenium_stealth import stealth
import base64
import os

options = webdriver.ChromeOptions()
# options.add_argument("--headless")  # Раскомментируйте, чтобы запускать без видимого окна
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

stealth(driver,
    languages=["en-US", "en"],
    vendor="Google Inc.",
    platform="Win32",
    webgl_vendor="Intel Inc.",
    renderer="Intel Iris OpenGL Engine",
    fix_hairline=True,
)

# chapter_counter = 1
page_counter = 1

js = """
    var url = arguments[0];
    var callback = arguments[1];

    fetch(url)
        .then(res => res.blob())
        .then(blob => {
            var reader = new FileReader();
            reader.readAsDataURL(blob);
            reader.onloadend = function() {
                // callback возвращает строку вида "data:image/jpeg;base64,/9j/4AAQ..."
                callback(reader.result);
            }
        });
"""

try:
    wait = WebDriverWait(driver, 10)

    driver.get("https://mangadex.org/chapter/4696b45a-ac45-48ae-a151-afdf63a5d3ca")

    open_menu_button = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "#__nuxt > div.flex.flex-grow.text-color > div.flex.flex-col.flex-grow > div.md-content.flex-grow > div > div.md--reader-chapter > div.reader--header.hide.md--reader-header > div.reader--header-meta > div.reader--meta.menu > svg"))) 
    open_menu_button.click()

    btn_scroll = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "#__nuxt > div.flex.flex-grow.text-color > div.flex.flex-col.flex-grow > div.md-content.flex-grow > div > div.md--reader-menu > div > div.flex.flex-col.gap-2 > button:nth-child(1)")))

    for i in range(2):
        btn_scroll.click()
        time.sleep(1.0)

    title_elem = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "#__nuxt > div.flex.flex-grow.text-color > div.flex.flex-col.flex-grow > div.md-content.flex-grow > div > div.md--reader-menu > div > div.flex.flex-col.gap-y-2.mb-2.md\:mb-4 > div:nth-child(1) > a")))
    title_name = title_elem.text.replace(' ', '_')

    save_dir = os.path.join(os.getcwd(), title_name)

    os.makedirs(save_dir, exist_ok=True)

    prev_chapter_num = "0"

    chapter_num = "-1"

    while(True):

        chapter_num_elem = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "#__nuxt > div.flex.flex-grow.text-color > div.flex.flex-col.flex-grow > div.md-content.flex-grow > div > div.md--reader-chapter > div.reader--header.hide.ls.md--reader-header > div.reader--header-meta > div.reader--meta.chapter")))

        # chapter_split = chapter_num_elem.text.split('.', 2)

        # chapter_num = chapter_split[len(chapter_split)-1].replace(' ','').replace('.', ',')

        chapter_num = chapter_num_elem.text.split("Ch.")[1].replace(' ','').replace('.', ',')

        if (chapter_num == prev_chapter_num):
            break

        prev_chapter_num = chapter_num

        chapter_dir = os.path.join(save_dir, chapter_num)

        os.makedirs(chapter_dir, exist_ok=True)

        imgs = wait.until(EC.visibility_of_all_elements_located((By.CLASS_NAME, "img")))

        for img in imgs:

            blob_url = img.get_attribute("src")

            data_uri = driver.execute_async_script(js, blob_url)

            if data_uri:
                base64_data = data_uri.split(',')[1]
                
                image_data = base64.b64decode(base64_data)
                
                with open(os.path.join(chapter_dir, f"{chapter_num}_{page_counter}.png"), "wb") as f:
                    f.write(image_data)

            page_counter += 1

        btn_chapter = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "#chapter-selector > a:nth-child(3)")))
        btn_chapter.click()

        #chapter_counter += 1
        page_counter = 1

        time.sleep(uniform(3.0, 5.0))

    print(f"Парсинг закончен на главе {chapter_num}!")
    
except Exception as e:
    print(f"Произошла ошибка: {e}")

finally:
    driver.quit()