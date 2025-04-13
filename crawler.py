#!/usr/bin/env python
import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from progress.bar import IncrementalBar
import time

WIKIPEDIA_URL = "https://en.wikipedia.org/wiki/Special:Random"
IMAGE_COUNT = 1
DATASET_FOLDER = "dataset"
FILE_EXTENSIONS = (".jpg", ".jpeg", ".png", ".gif")
MIN_HEIGHT = 200
MIN_WIDTH = 200
# Wikipedia API query string to get the main image on a page
# (partial URL will be added to the end)
IMAGE_QUERY_URL = 'http://en.wikipedia.org/w/api.php?action=query&prop=pageimages&format=json&piprop=original&titles='

# Wikipedia images varies in size and extraction doesn't diferentiate between icons, flags, small images.
# in my scenario I am mostly interested in images of at least 200x200 pixels and 1 image per topic.
def extract_images_from_url(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    print(soup)
    images = []
    for img in soup.find_all('img'):
        print(img.parent)
        parentA = img.parent
        if parentA.name == 'a':
            # print(parentA)
            img_url = urljoin(url, parentA['src'])
        # if img_url.endswith(FILE_EXTENSIONS) and int(img['height']) >= MIN_HEIGHT and int(img['width']) >= MIN_WIDTH:
            images.append(img_url)
    return images

def fetch_random_wikipedia_article():
    response = requests.get(WIKIPEDIA_URL)
    return response.url

def create_dataset_folder():
    if not os.path.exists(DATASET_FOLDER):
        os.makedirs(DATASET_FOLDER)

def save_images(images):
    for img_url in images:
        download_image(img_url, DATASET_FOLDER)

def save_image(img_url):
    download_image(img_url, DATASET_FOLDER)
        
def download_image(img_url, folder, retry_count=0):
    try:
        print (f"START Downloading: {img_url}")
        headers = {'User-Agent': 'CoolBot/0.0 (https://example.org/coolbot/; coolbot@example.org)'}
        response = requests.get(img_url, stream=True, headers=headers)
        if response.status_code == 200:
            # Extract the image filename from the URL
            filename = os.path.basename(img_url)
            filepath = os.path.join(folder, filename)
            print(f"Downloaded: {filename}")

            
            # Save the image to the specified folder
            with open(filepath, 'wb') as file:
                for chunk in response.iter_content(4096):
                    file.write(chunk)
        else:
            print(f"Failed to download {img_url}: {response.status_code}")
            # Retry as probably request was blocked with 403
            if retry_count < 2:
                print(f"Retrying {img_url} ({retry_count + 1}/2)")
                time.sleep(2)
                download_image(img_url, folder, retry_count + 1)
    except Exception as e:
        print(f"Failed to download {img_url}: {e}")

def main():
    bar = IncrementalBar('Downloading', max=IMAGE_COUNT)
    create_dataset_folder()
    images_fetched = set()
    
    while len(images_fetched) < IMAGE_COUNT:
        url = fetch_random_wikipedia_article()
        print(f"Fetching URL: {url}")
        images = extract_images_from_url(url)
        # there might be more than one image in the page
        if (len(images) > 0):
            for img_url in images:
                if img_url not in images_fetched:
                    images_fetched.add(img_url)
                    save_image(img_url)
                    # print(f"Downloaded: {img_url}")
                    bar.next()
                    
    bar.finish()

if __name__ == "__main__":
    main()