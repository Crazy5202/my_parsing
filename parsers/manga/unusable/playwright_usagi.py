from playwright.sync_api import sync_playwright
from playwright_stealth import Stealth

CHAPTER_LINK = 'https://web.usagi.one/aqua/vol1/1'

with sync_playwright() as p:
    browser = p.chromium.launch(
        channel = 'opera',
        headless=False,
        args=['--disable-blink-features=AutomationControlled']
    )
    context = browser.new_context(
        viewport={'width': 1920, 'height': 1080},
        locale='ru-RU',
        timezone_id='Europe/Moscow',
        user_agent=('Mozilla/5.0 (Windows NT 10.0; Win64; x64)'),
    )
    Stealth().apply_stealth_sync(context)
    page = browser.new_page()

    page.goto(CHAPTER_LINK)

    ### GETTING TITLE AND CREATING DIR
    title_elem = page.wait_for_selector('#mangaBox h1 a', state='visible', timeout=10)
    title_name = (title_elem.text_content() or '').replace(' ', '_')
    print(title_name)