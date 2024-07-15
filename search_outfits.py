import requests
from bs4 import BeautifulSoup
from requests.exceptions import HTTPError
import requests
import os
import urllib.request
import re
import shutil
save_folder = "static/images"

def clear_images_folder():
    
    if os.path.exists(save_folder):
        shutil.rmtree(save_folder)
    os.makedirs(save_folder, exist_ok=True)

# Function to search for Myntra outfits based on predefined colors and gender
def search_outfits(colors, gender):
    base_url = "https://www.google.com/search?q="
    links = []
    links_per_color = 5

    for c in colors:
        print(f"Searching for outfits for the color {c}...")
        color_links = []
        try:
            search_query = f"myntra {gender} outfits in {c} color"
            search_url = base_url + search_query.replace(" ", "+")
            response = requests.get(search_url)
            soup = BeautifulSoup(response.content, 'html.parser')

            for link in soup.find_all('a'):
                if 'href' in link.attrs and '/url?q=' in link['href']:
                    actual_url = link['href'].split('/url?q=')[1].split('&')[0]
                    if 'myntra.com/' in actual_url and 'buy' in actual_url:
                        print(f"Found link: {actual_url}")
                        color_links.append(actual_url)
                        if len(color_links) >= links_per_color:
                            break
            if len(color_links) > 0:
                links.extend(color_links[:links_per_color])
        except Exception as e:
            print(f"Error occurred while searching for {c} color: {e}")

    return links



# Predefined colors and gender
colors = ['red', 'blue', 'green', 'yellow']
gender = 'women'  # Replace with 'men' if needed

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

def fetch_image_urls(search_term, num_images_to_download=1):
    url = f"https://www.bing.com/images/search?q={search_term}&first=1"
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    soup = BeautifulSoup(response.content, 'html.parser')
    img_tags = soup.find_all('img', class_='mimg')

    img_urls = []
    for img in img_tags:
        img_urls.append(img.get('src'))

    return img_urls[:num_images_to_download]

def extract_product_details(outfit_links):
    products = []
    for link in outfit_links:
        # link = outfit['link']
        # color = outfit['color']

        try:
            pattern = r'myntra\.com/([^/]+)/([^/]+)/([^/]+)'
            match = re.search(pattern, link)
            if match:
                product_type = match.group(1)
                product_company = match.group(2)
                product_title = match.group(3)
                image_url=''
                products.append({
                    'link':link,
                    'product_type': product_type,
                    'product_company': product_company,
                    'product_title': product_title,
                    'image_url':image_url
                })
            else:
                print(f"No match found in link: {link}")
        except Exception as e:
            print(f"Error occurred while extracting details from {link}: {e}")

    return products

def download_images(image_url,i):
   
    os.makedirs(save_folder, exist_ok=True)
   
    
    filename = os.path.join(save_folder, f"{i}.jpg")
    urllib.request.urlretrieve(image_url, filename)

    relative_path = os.path.join("images", f"{i}.jpg")
    return relative_path.replace("\\", "/")