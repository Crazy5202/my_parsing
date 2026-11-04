import nodriver as uc
import time
from random import uniform
import base64
import os

CHAPTER_LINK = 'https://mangalib.me/ru/1092--aria/read/v12/c63'

def transform_chapter_str(chapter_str: str, digit_count: str = 5) -> str:
    chapter_num = chapter_str.split(".")[0]
    diff = digit_count - len(chapter_num)
    if (diff > 0):
        chapter_str = "0"*diff + chapter_str.replace('.', ',')
    return chapter_str

def transform_page_str(page_str: str, digit_count: str = 3) -> str:
    diff = digit_count - len(page_str)
    if (diff > 0):
        page_str = "0"*diff + page_str
    return page_str

JS_FETCH_BLOB = """
    (async () => {
        const res = await fetch('%s');
        const blob = await res.blob();
        return new Promise((resolve) => {
            const reader = new FileReader();
            reader.onloadend = () => resolve(reader.result);
            reader.readAsDataURL(blob);
        });
    })()
"""

async def main():
    try:
        ### SETUP
        browser = await uc.start(
            headless=False,
            browser_executable_path=None,
        )

        #page = await browser.get("https://www.browserscan.net/bot-detection")
        page = await browser.get(CHAPTER_LINK)

        time.sleep(uniform(1.0, 2.0))

        await page.scroll_up(500)

        time.sleep(uniform(1.0, 2.0))

        cookie_button = await page.find('//*[@id="app"]/div[3]/div/div/div/div[2]/div[2]/button', timeout=10)
        await cookie_button.mouse_click()

        ### GETTING TITLE AND CREATING DIR
        title_elem = await page.find('//*[@id="app"]/div[1]/header/div/a/div[2]', timeout=10)
        title_name = title_elem.text.replace(' ', '_')
    
        save_dir = os.path.join(os.getcwd(), title_name)
    
        os.makedirs(save_dir, exist_ok=True)

        chapter_num = -1 # На всякий случай, чтобы не получить ошибку в случае запуска на другой странице
    
        while(True):
            ### GETTING CHAPTER NUM OR STOPPING
            chapter_num_elem = await page.find('//*[@id="app"]/div[1]/header/div/a/div[3]', timeout=10)
            if not chapter_num_elem:
                reviews = await page.find('//*[@id="app"]/div[1]/div[2]/div[6]/div[1]/div/div[4]/span/text()', timeout = 10)
                if reviews:
                    break
                else:
                    print("ERROR: не найдена глава, не найдено условие парсинга")
    
            # EXTRACTING THE CHAPTER NUM OUT OF THE STRING
            chapter_num = chapter_num_elem.text.split("Глава")[1][1:]
    
            time.sleep(uniform(1.0, 2.0))
    
            ### GETTING CHAPTER NUM AND MAKING DIR
            chapter_dir = os.path.join(save_dir, transform_chapter_str(chapter_num,))
    
            os.makedirs(chapter_dir, exist_ok=True)
    
            ### GETTING PAGES OF CHAPTER FOR TRACKING
            max_page_elem = await page.find('//*[@id="app"]/div[1]/main/div/footer/label/text()', timeout = 10)
            max_page = int(max_page_elem.text.split("/")[1][1:])
    
            ### SAVING IMAGES AND NEXT PAGING
            for i in range(1, max_page+1):
                img = await page.find(f'//*[@id="app"]/div[1]/main/div/div[{i}]/img', timeout=10)
    
                blob_url = img['src']

                js_code = JS_FETCH_BLOB % blob_url

                data_uri = await page.evaluate(js_code, await_promise=True)
    
                if data_uri:
                    base64_data = data_uri.split(',')[1]
                    image_data = base64.b64decode(base64_data)
                    with open(os.path.join(chapter_dir, f"{transform_page_str(str(i))}.png"), "wb") as f:
                        f.write(image_data)

                next_page_btn = await page.find(f'//*[@id="app"]/div[1]/main/div/div[{max_page+1}]/div/div[2]', timeout = 10)
                await next_page_btn.mouse_click()
                time.sleep(uniform(2.0, 3.0))
        
        print(f"Парсинг закончен на главе {chapter_num}!")

    except Exception as e:
        print(f"Ошибка: {e}")

    finally:
        try:
            for tab in browser.tabs:
                await tab.aclose()
            if browser.connection:
                await browser.connection.aclose()
            browser.stop()
        except Exception as e:
            print(f"Ошибка при закрытии браузера: {e}")

if __name__ == "__main__":
    uc.loop().run_until_complete(main())