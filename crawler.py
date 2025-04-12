#!/usr/bin/env python
import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

WIKIPEDIA_URL = "https://en.wikipedia.org/wiki/Special:Random"
IMAGE_COUNT = 10
DATASET_FOLDER = "dataset"
FILE_EXTENSIONS = (".jpg", ".jpeg", ".png", ".gif")
MIN_HEIGHT = 150
MIN_WIDTH = 150

# Wikipedia images varies in size and extraction doesn't diferentiate between icons, flags, small images.
# in my scenario I am mostly interested in images of at least 200x200 pixels and 1 image per topic.
def extract_images_from_url(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    images = []
    for img in soup.find_all('img'):
        img_url = urljoin(url, img['src'])
        if img_url.endswith(FILE_EXTENSIONS) and int(img['height']) >= MIN_HEIGHT and int(img['width']) >= MIN_WIDTH:
            images.append(img_url)
    return images

def fetch_random_wikipedia_url():
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
        
def download_image(img_url, folder):
    try:
        response = requests.get(img_url, stream=True)
        if response.status_code == 200:
            # Extract the image filename from the URL
            filename = os.path.basename(img_url)
            filepath = os.path.join(folder, filename)
            
            # Save the image to the specified folder
            with open(filepath, 'wb') as file:
                for chunk in response.iter_content(1024):
                    file.write(chunk)
    except Exception as e:
        print(f"Failed to download {img_url}: {e}")

def main():
    create_dataset_folder()
    images_fetched = set()
    
    while len(images_fetched) < IMAGE_COUNT:
        url = fetch_random_wikipedia_url()
        # if url not in urls_fetched:
        # urls_fetched.add(url)
        images = extract_images_from_url(url)
        if (images):
            for img_url in images:
                images_fetched.add(img_url)
                save_image(img_url)

if __name__ == "__main__":
    main()