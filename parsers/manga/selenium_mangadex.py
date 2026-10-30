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
from dotenv import load_dotenv

CHAPTER_LINK = 'https://mangadex.org/chapter/efcbbed4-5a28-482a-b519-99526207c292'
START_CHAPTER_NUM = "10"

load_dotenv()
LOGIN = os.getenv("MG_LOGIN")
PASSWORD = os.getenv("MG_PASSWORD")

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

def smooth_scroll(driver, speed=200):
    last_height = driver.execute_script("return document.body.scrollHeight")
    current_position = 0
    
    while current_position < last_height:
        driver.execute_script(f"window.scrollBy(0, {speed});")
        current_position += speed
        time.sleep(0.1)
        
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height > last_height:
            last_height = new_height

def smooth_scroll_up(driver, speed=200):
    while True:
        current_position = driver.execute_script("return window.pageYOffset")
        if current_position <= 0:
            break
        step = min(speed, current_position)
        driver.execute_script(f"window.scrollBy(0, -{step});")
        time.sleep(0.1)

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

    driver.get(CHAPTER_LINK)

    smooth_scroll_up(driver) 

    #Логин
    login_button = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "#avatar")))
    login_button.click()
    time.sleep(2.0)

    login_button = driver.find_element(By.XPATH, '//*[@id="app"]/div[5]/div[2]/div/div[1]/button[3]')
    login_button.click()
    time.sleep(2.9)

    login_form = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "#username")))
    login_form.send_keys(LOGIN)
    time.sleep(1.1)

    login_form = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "#password")))
    login_form.send_keys(PASSWORD)
    time.sleep(1.2)

    login_button = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "#kc-login")))
    login_button.click()
    time.sleep(3.3)

    open_menu_button = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "#app > div.flex.grow.text-color > div.flex.flex-col.grow > div.md-content.grow > div > div.md--reader-chapter > div.reader--header.hide.md--reader-header > div.reader--header-meta > div.reader--meta.menu"))) 
    open_menu_button.click()

    btn_scroll = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "#app > div.flex.grow.text-color > div.flex.flex-col.grow > div.md-content.grow > div > div.md--reader-menu > div > div.flex.flex-col.gap-2 > button:nth-child(1)")))

    for i in range(2):
        btn_scroll.click()
        time.sleep(1.0)

    title_elem = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "#app > div.flex.grow.text-color > div.flex.flex-col.grow > div.md-content.grow > div > div.md--reader-chapter > div.reader--header.hide.md--reader-header > div.grow > a")))
    title_name = title_elem.text.replace(' ', '_')

    save_dir = os.path.join(os.getcwd(), title_name)

    os.makedirs(save_dir, exist_ok=True)

    prev_chapter_num = "-1"

    found_flag = False

    while(True):
        chapter_num_elem = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "#app > div.flex.grow.text-color > div.flex.flex-col.grow > div.md-content.grow > div > div.md--reader-chapter > div.reader--header.hide.ls.md--reader-header > div.reader--header-meta > div.reader--meta.chapter")))

        chapter_num = chapter_num_elem.text.split("Ch.")[1].replace(' ','').replace('.', ',')

        if (chapter_num == prev_chapter_num):
            break

        prev_chapter_num = chapter_num

        if ((not START_CHAPTER_NUM == "-1") and found_flag == False and chapter_num != START_CHAPTER_NUM):
            btn_chapter = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "#chapter-selector > a:nth-child(3)")))
            btn_chapter.click()
            time.sleep(uniform(1.0, 2.0))
            continue

        found_flag = True

        time.sleep(uniform(3.0, 5.0))

        smooth_scroll(driver)

        time.sleep(uniform(2.0, 3.0))

        #driver.execute_script("window.scrollTo(0, 0);")

        chapter_dir = os.path.join(save_dir, transform_chapter_str(chapter_num,))

        os.makedirs(chapter_dir, exist_ok=True)

        imgs = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "img")))

        max_page_elem = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "#app > div.flex.grow.text-color > div.flex.flex-col.grow > div.md-content.grow > div > div.md--reader-chapter > div.reader--header.hide.ls.md--reader-header > div.reader--header-meta > div.reader--meta.page")))
        max_page = int(max_page_elem.text.split('/')[1])

        if (len(imgs) < max_page):
            print(f"WARNING: Only parsed {len(imgs)}/{max_page} pages for chapter {chapter_num}!")

        for img in imgs:

            blob_url = img.get_attribute("src")

            data_uri = driver.execute_async_script(js, blob_url)

            if data_uri:
                base64_data = data_uri.split(',')[1]
                
                image_data = base64.b64decode(base64_data)
                
                with open(os.path.join(chapter_dir, f"{transform_page_str(str(page_counter))}.png"), "wb") as f:
                    f.write(image_data)

            page_counter += 1

        print(f"Succcess: parsed {len(imgs)} pages for chapter {chapter_num}")

        btn_chapter = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "#chapter-selector > a:nth-child(3)")))
        btn_chapter.click()

        page_counter = 1

    print(f"Парсинг закончен на главе {chapter_num}!")
    
except Exception as e:
    print(f"Произошла ошибка: {e}")

finally:
    driver.quit()