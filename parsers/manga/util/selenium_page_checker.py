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

def transform_chapter_str(chapter_str: str, digit_count: str = 5) -> str:
    chapter_num = chapter_str.split(",")[0]
    diff = digit_count - len(chapter_num)
    if (diff > 0):
        chapter_str = "0"*diff + chapter_str
    return chapter_str

def transform_page_str(page_str: str, digit_count: str = 3) -> str:
    diff = digit_count - len(page_str)
    if (diff > 0):
        page_str = "0"*diff + page_str
    return page_str

# chapter_counter = 1
page_counter = 0

try:
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
    wait = WebDriverWait(driver, 10)

    driver.get('https://mangadex.org/chapter/61394a0e-6600-44d5-b00f-27fa29a9932b')
    #driver.get("https://mangadex.org/chapter/4696b45a-ac45-48ae-a151-afdf63a5d3ca")

    open_menu_button = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "#__nuxt > div.flex.flex-grow.text-color > div.flex.flex-col.flex-grow > div.md-content.flex-grow > div > div.md--reader-chapter > div.reader--header.hide.md--reader-header > div.reader--header-meta > div.reader--meta.menu > svg"))) 
    open_menu_button.click()

    title_elem = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "#__nuxt > div.flex.flex-grow.text-color > div.flex.flex-col.flex-grow > div.md-content.flex-grow > div > div.md--reader-menu > div > div.flex.flex-col.gap-y-2.mb-2.md\:mb-4 > div:nth-child(1) > a")))
    title_name = title_elem.text.replace(' ', '_')

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

        time.sleep(uniform(1.0, 2.0))

        max_page_elem = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "#__nuxt > div.flex.flex-grow.text-color > div.flex.flex-col.flex-grow > div.md-content.flex-grow > div > div.md--reader-chapter > div.reader--header.hide.ls.md--reader-header > div.reader--header-meta > div.reader--meta.page")))
        max_page = int(max_page_elem.text.split('/')[1])

        page_counter += max_page

        btn_chapter = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "#chapter-selector > a:nth-child(3)")))
        btn_chapter.click()

    print(f"Для {title_name} всего страниц: {page_counter}")
    
except Exception as e:
    print(f"Произошла ошибка: {e}")

finally:
    driver.quit()