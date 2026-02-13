import requests
import time
from bs4 import BeautifulSoup

# should to try out this with authorization through selenium + implement timeouts, random sleep (basically stuff from IMDB_parser)

f = open('Ark.txt', 'w', encoding="utf-8")
url = "https://www.royalroad.com/fiction/76463/mage-tank/chapter/1394181/1-a-deadly-oak-tree"
while True:
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    text = soup.get_text()
    zero_pos = text.find("notifications")-90
    first_pos = text.find("Next Chapter")+13
    second_pos = text.find("PayPal")
    trimmed_text = (text[8:zero_pos] + text[first_pos:second_pos]).replace('Advertisement Remove', '')
    while '\n\n\n\n' in trimmed_text:
        trimmed_text = trimmed_text.replace("\n\n\n\n", "\n\n\n")
    f.write(trimmed_text)
    url = soup.find("div", class_="row nav-buttons").contents[-2].contents[1].get('href')
    if url is None:
        break
    url = 'https://www.royalroad.com' + url
    time.sleep(1)
f.close()