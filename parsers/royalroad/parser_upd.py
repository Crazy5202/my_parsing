import requests
import time
from bs4 import BeautifulSoup
import os
from kivy.utils import platform
import re
from pprint import pprint

# should to try out this with authorization through selenium + implement timeouts, random sleep (basically stuff from IMDB_parser)
DATA_FOLDER = ''
if platform == 'android':
    DATA_FOLDER = os.getenv('EXTERNAL_STORAGE') + '/'
f = open(DATA_FOLDER+'Parsed_book.txt', 'w', encoding="utf-8")
url = "https://www.royalroad.com/fiction/70174/accidental-war-mage-book-1-stubs-on-march-28th/chapter/1763020/appendix-a-notes-on-geography"
counter = 1
while True:
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    pattern = re.compile('Amazon')

    # Peter's suggestion here returns a list of what appear to be strings
    columns = soup.findAll(string=pattern)

    # you can reach the tag using one of the convenience attributes seen here
    pprint(columns[0].__dict__)

    pprint(soup)

    text = soup.get_text()
    zero_pos = text.find("notifications")-90
    first_pos = text.find("Next Chapter")+13
    trimmed_text = (text[8:zero_pos] + text[first_pos:]).replace('Advertisement Remove', '')
    second_pos = trimmed_text.find("Previous Chapter")
    trimmed_text = trimmed_text[:second_pos]
    while '\n\n\n\n' in trimmed_text:
        trimmed_text = trimmed_text.replace("\n\n\n\n", "\n\n\n")
    f.write(trimmed_text)
    print(f"Webpage {counter} parsed")
    counter += 1
    url = soup.find("div", class_="row nav-buttons").contents[-2].contents[1].get('href')
    if url is None:
        break
    url = 'https://www.royalroad.com' + url
    time.sleep(1)
f.close()