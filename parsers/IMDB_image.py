import pandas as pd
from bs4 import BeautifulSoup
import requests
import os
import random
import time

previews_dir = os.path.join(os.getcwd(), "previews")

os.makedirs(previews_dir, exist_ok=True)

def file_saver(url, index) -> bool:
    connect_timeout = 100
    read_timeout = 100

    headers={'User-Agent':'Mozilla/5.0 (Windows NT 6.3; Win 64 ; x64) Apple WeKit /537.36(KHTML , like Gecko) Chrome/80.0.3987.162 Safari/537.36'} 
    response = requests.get(url, headers=headers, verify=False, timeout=(connect_timeout, read_timeout))

    if response.status_code == 200:
        html_content = response.text
    else:
        #print("Failed to fetch the webpage")
        return False

    soup = BeautifulSoup(html_content, "html.parser")

    first_media_div = soup.find('div', class_='ipc-media')

    if first_media_div:
        if 'src' not in first_media_div.contents[0].attrs:
            return False
        img_url = first_media_div.contents[0].attrs['src']
        #print(f"Image URL: {img_url}")
    else:
        #print("Image not found")
        return False


    image_response = requests.get(img_url, verify=False, timeout=(connect_timeout, read_timeout))

    if image_response.status_code == 200:
    
        filename = os.path.join(previews_dir, f"{index}.jpg")
        with open(filename, "wb") as f:
            for chunk in image_response.iter_content(1024):
                f.write(chunk)
        #print(f"Image saved as {filename}")
    else:
        #print("Failed to download the image")
        return False

def process_row(row):
    print(f"Processing row: {row['movieId']}, {row['imdbId']}")
    wait_time = random.uniform(0, 3)
    time.sleep(wait_time)
    str_imdb = str(row['imdbId'])
    res = file_saver('https://www.imdb.com/title/tt'+'0'*(7-len(str_imdb))+str_imdb, str(row['movieId']))
    if res == False:
        with open("fails.txt", "a") as file:
            file.write(f"{row['movieId']}\n")

def main():
    df = pd.read_csv('link.csv')
    df = df[['movieId', 'imdbId']]

    ## ТУТ!!!

    start_index = 9101
    end_index = 10400
    df.iloc[(start_index-1):end_index].apply(process_row, axis=1)

if __name__ == "__main__":
    main()