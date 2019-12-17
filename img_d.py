import requests
import os
import json
from typing import List


def get_content(url):
    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()
    except requests.Timeout:
        print(f"timeout error: {url}")
    except requests.HTTPError as err:
        code = err.response.status_code
        print(f"error url: {url}, code: {code}")
    except requests.RequestException:
        print(f"download error url: {url}")
    else:
        return response.content


def save_image(image, filepath):
    with open(filepath, "wb") as f:
        f.write(image)


def fetch_spacex_last_launch() -> List:
    url = 'https://api.spacexdata.com/v3/launches/'
    launches = json.loads(get_content(url))[::-1]
    for launch in launches:
        images = launch.get("links").get("flickr_images")
        if images:
            break
    return images


def save_images(image_urls, directory):
    if not os.path.exists(directory):
        os.makedirs(directory)
    for num, image_url in enumerate(image_urls):
        image = get_content(image_url)
        filepath = f"{directory}/spacex{num+1}.jpg"
        save_image(image, filepath)

if __name__ == "__main__":
    #directory = "images"
    #filename = "hubble.jpg"
    #url = "https://upload.wikimedia.org/wikipedia/commons/3/3f/HST-SM4.jpeg"
    #picture = get_content(url)
    #file_path = directory + "/" + filename
    #save_image(picture, file_path)
    image_urls = fetch_spacex_last_launch()
    save_images(image_urls, "images")
