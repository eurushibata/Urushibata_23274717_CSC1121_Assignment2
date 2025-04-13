#!/usr/bin/env python
import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from progress.bar import IncrementalBar
import time
import json

WIKIPEDIA_URL = "https://en.wikipedia.org/wiki/Special:Random"
IMAGE_COUNT = 5000
DATASET_FOLDER = "dataset"
# FILE_EXTENSIONS = (".jpg", ".jpeg", ".png", ".gif")

# Wikipedia API query string to get the main image on a page
# (partial URL will be added to the end)
IMAGE_QUERY_URL = 'http://en.wikipedia.org/w/api.php?action=query&prop=pageimages&format=json&piprop=original&titles='

def get_page_info(url):
    response = requests.get(url)
    page_content = BeautifulSoup(response.text, 'html.parser')
    # Check if the article has an image
    first_heading = page_content.find('h1', class_='firstHeading')
    title_text = ""
    span = first_heading.find("span")
    i = first_heading.find("i")
    if (span):
        title_text = span.text
    elif (i):
        title_text = i.text
    # print (title_text)

    # now that we have the title we can query the Wikipedia API
    url = IMAGE_QUERY_URL + title_text
    response = requests.get(url)
    data = response.json()
    # print (data['query']['pages'])
    page_data = data['query']['pages']
    for page_id, page_info in page_data.items():
        if 'original' in page_info:
            image_url = page_info['original']['source']
            content = page_content.find('div', id='mw-content-text').findAll('p')
            # print(f"Image URL: {image_url}")
            return {
                "image_url": image_url,
                "image_name": os.path.basename(image_url),
                "wikipedia_source_url": url,
                "title": title_text,
                "content": content
            }
        else:
            # print("No image found for this article.")
            return None    

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
        # print (f"START Downloading: {img_url}")
        headers = {'User-Agent': 'CoolBot/0.0 (https://example.org/coolbot/; coolbot@example.org)'}
        response = requests.get(img_url, stream=True, headers=headers)
        if response.status_code == 200:
            # Extract the image filename from the URL
            filename = os.path.basename(img_url)
            filepath = os.path.join(folder, filename)
            # print(f"Downloaded: {filename}")

            
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

def save_record_to_file(record, index, filename):
    title = record['title']
    image_url = record['image_url']
    image_name = record['image_name']
    wikipedia_source_url = record['wikipedia_source_url']
    content = record['content']
    
    filename = os.path.join(DATASET_FOLDER, filename)
    
    with open(filename, 'a', encoding='utf-8') as file:
        file.write("<doc>\n")
        file.write(f"<docno>{index}</docno>\n")
        file.write(f"<title>{title}</title>\n")
        file.write(f"<img_loc>{image_name}</img_loc>\n")
        file.write(f"<bib>{wikipedia_source_url}</bib>\n")
        file.write(f"<text>{title}\n")
        for paragraph in content:
            file.write(paragraph.text + "\n")
        file.write(f"</text>\n")    
        file.write("</doc>\n")

def save_record_to_file_json(records, filename):
    # prepare content
    for record in records:
        content_text = ""
        for paragraph in record['content']:
            content_text+= paragraph.text + "\n"
        record['content'] = content_text

    filename = os.path.join(DATASET_FOLDER, filename)

    with open(filename, 'w', encoding='utf-8') as file:
        json.dump(records, file, indent=2, ensure_ascii=False)

def main():
    bar = IncrementalBar('Downloading', max=IMAGE_COUNT)
    create_dataset_folder()
    images_fetched = set()
    images_fetched_json = []
    
    while len(images_fetched) < IMAGE_COUNT:
        url = fetch_random_wikipedia_article()
        # print(f"Fetching URL: {url}")
        content = get_page_info(url)
        if (content):
            if content['image_url'] not in images_fetched:
                save_image(content['image_url'])
                images_fetched.add(content['image_url'])
                # print(f"Downloaded: {image_url}")
                save_record_to_file(content, len(images_fetched), "0.wikipedia.images.xml")
                content['docno'] = len(images_fetched)
                images_fetched_json.append(content)
                bar.next()
    save_record_to_file_json(images_fetched_json, "0.wikipedia.images.json")
    bar.finish()

if __name__ == "__main__":
    main()