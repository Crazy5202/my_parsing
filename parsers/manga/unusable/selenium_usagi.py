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

CHAPTER_LINK = 'https://web.usagi.one/aqua/vol1/1'

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
    ### SETUP
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

    driver.get("https://www.browserscan.net/bot-detection")

    ### GETTING TITLE AND CREATING DIR
    title_elem = wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="mangaBox"]/h1/a')))
    title_name = title_elem.text.replace(' ', '_')

    save_dir = os.path.join(os.getcwd(), title_name)

    os.makedirs(save_dir, exist_ok=True)

    prev_chapter_num = "-1"

    while(True):
        ### GETTING CHAPTER NUM OR STOPPING
        try:
            chapter_num_elem = wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="mangaBox"]/h1/text()[2]')))
        except Exception as e1:
            try:
                similar_entries = wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="mangaBox"]/div[2]/div[2]/div[1]/div[1]/h3/a/span')))
                break
            except Exception as e2:
                print('END STATE ERRORS:\n', e1, '\n', e2)
                raise e1

        # CHECKING WHETHER THE CHAPTER IS EXTRA
        if "Экстра" in chapter_num_elem:
            if prev_chapter_num[-1] == ",":
                prev_chapter_num_split = prev_chapter_num.rsplit(",")
                chapter_num = prev_chapter_num_split[0] + str(int(prev_chapter_num_split[1])+1)
            else:
                chapter_num = prev_chapter_num + ",1"

        # EXTRACTING THE CHAPTER NUM OUT OF THE STRING
        chapter_num = chapter_num_elem.split("-")[1]
        chapter_num = chapter_num[1:].split(" ")[0]

        prev_chapter_num = chapter_num

        time.sleep(uniform(0.5, 2.0))

        ### GETTING CHAPTER NUM AND MAKING DIR
        chapter_dir = os.path.join(save_dir, transform_chapter_str(chapter_num,))

        os.makedirs(chapter_dir, exist_ok=True)

        ### Plan: 1. Get max_page 2. for(max_page) with saving and pushing button
        max_page_elem = wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="wrap"]/div[8]/div[2]/div/div[2]/span[2]')))
        max_page = int(max_page_elem.text)

        ### SAVING IMAGES AND NEXT PAGING
        for i in range(1, max_page+1):
            img = wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="mangaPicture"]')))

            blob_url = img.get_attribute("src")

            data_uri = driver.execute_async_script(js, blob_url)

            if data_uri:
                base64_data = data_uri.split(',')[1]
                
                image_data = base64.b64decode(base64_data)
                
                with open(os.path.join(chapter_dir, f"{transform_page_str(str(i))}.png"), "wb") as f:
                    f.write(image_data)

            img.click()

    print(f"Парсинг закончен на главе {chapter_num}!")
    
except Exception as e:
    print(f"Произошла ошибка: {e}")

finally:
    driver.quit()