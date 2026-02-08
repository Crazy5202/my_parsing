from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from random import uniform
from selenium_stealth import stealth
import requests
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

save_dir = os.path.join(os.getcwd(), "manga")

os.makedirs(save_dir, exist_ok=True)

chapter_counter = 1
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

    driver.get("https://mangadex.org/chapter/61394a0e-6600-44d5-b00f-27fa29a9932b")

    open_menu_button = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "#__nuxt > div.flex.flex-grow.text-color > div.flex.flex-col.flex-grow > div.md-content.flex-grow > div > div.md--reader-chapter > div.reader--header.hide.md--reader-header > div.reader--header-meta > div.reader--meta.menu > svg"))) 
    open_menu_button.click()

    #btn_next = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "#__nuxt > div.flex.flex-grow.text-color > div.flex.flex-col.flex-grow > div.md-content.flex-grow > div > div.md--reader-menu > div > div:nth-child(3) > button:nth-child(3)")))

    #btn_next = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "#__nuxt > div.flex.flex-grow.text-color > div.flex.flex-col.flex-grow > div.md-content.flex-grow > div > div.md--reader-chapter > div.min-w-0.relative.pages-wrap.md--reader-pages > div.overflow-x-auto.flex.items-center.h-full.select-none > div")))

    btn_scroll = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "#__nuxt > div.flex.flex-grow.text-color > div.flex.flex-col.flex-grow > div.md-content.flex-grow > div > div.md--reader-menu > div > div.flex.flex-col.gap-2 > button:nth-child(1)")))

    for i in range(2):
        btn_scroll.click()
        time.sleep(1.0)

    #btn_fit = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "#__nuxt > div.flex.flex-grow.text-color > div.flex.flex-col.flex-grow > div.md-content.flex-grow > div > div.md--reader-menu > div > div.flex.flex-col.gap-2 > div:nth-child(2) > button.flex-grow.mr-2.rounded.custom-opacity.relative.md-btn.flex.items-center.px-3.overflow-hidden.accent.px-4.flex-grow.mr-2")))
    #btn_fit.click()

    close_menu_button = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "#__nuxt > div.flex.flex-grow.text-color > div.flex.flex-col.flex-grow > div.md-content.flex-grow > div > div.md--reader-menu > div > div.flex.justify-between.-mx-2.-mt-2 > button")))
    close_menu_button.click()

    while(True):

        imgs = wait.until(EC.visibility_of_all_elements_located((By.CLASS_NAME, "img")))

        #img = driver.find_element(By.CLASS_NAME, "img")

        #imgs = driver.find_elements(By.CLASS_NAME, "img")

        for img in imgs:
            #     img.screenshot(f"./frames/{chapter_counter}_{page_counter}.png")

            blob_url = img.get_attribute("src")

            data_uri = driver.execute_async_script(js, blob_url)

            if data_uri:
                # Обрезаем начало "data:image/jpeg;base64,"
                # Разделяем по запятой и берем вторую часть
                base64_data = data_uri.split(',')[1]
                
                # Декодируем
                image_data = base64.b64decode(base64_data)
                
                with open(os.path.join(save_dir, f"{chapter_counter}_{page_counter}.png"), "wb") as f:
                    f.write(image_data)

            page_counter += 1

        #btn = wait.until(EC.visibility_of_element_located((By.NAME, "data-v-d82f1958")))
        #btn_next = driver.find_element(By.XPATH, "//button[.//path[contains(@d, 'm10 18 6-6-6-6')]]")
        #buttons = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "button")))

        #buttons = driver.find_elements(By.CLASS_NAME, "button")
        
        #print(len(buttons))

        #flex = driver.find_element(By.NAME, "flex")

        # flex = wait.until(EC.presence_of_element_located((By.NAME, "flex")))

        # buttons = flex.find_elements(By.CLASS_NAME, "button")
        
        # print(len(buttons))

        #btn_next.click()
        open_menu_button = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "#__nuxt > div.flex.flex-grow.text-color > div.flex.flex-col.flex-grow > div.md-content.flex-grow > div > div.md--reader-chapter > div.reader--header.hide.md--reader-header > div.reader--header-meta > div.reader--meta.menu > svg"))) 
        open_menu_button.click()

        btn_chapter = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "#chapter-selector > a:nth-child(3)")))
        btn_chapter.click()
        
        close_menu_button = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "#__nuxt > div.flex.flex-grow.text-color > div.flex.flex-col.flex-grow > div.md-content.flex-grow > div > div.md--reader-menu > div > div.flex.justify-between.-mx-2.-mt-2 > button")))
        close_menu_button.click()

        chapter_counter += 1
        page_counter = 1

        time.sleep(uniform(3.0, 5.0))
    
except Exception as e:
    print(f"Произошла ошибка: {e}")

finally:
    time.sleep(5)
    driver.quit()