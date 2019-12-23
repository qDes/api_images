import requests
import os
import json

from typing import List
from PIL import Image

def get_content(url, payload={}):
    try:
        cafile = 'cacert.pem' # http://curl.haxx.se/ca/cacert.pem
        response = requests.get(url, timeout=30, verify=cafile,
                                params=payload)
        response.raise_for_status()
    except requests.Timeout:
        print(f"timeout error: {url}")
    except requests.HTTPError as err:
        code = err.response.status_code
        print(f"error url: {url}, code: {code}")
    except requests.RequestException as err:
        print(f"{err} error; url: {url}")
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


def get_extension(url):
    ext = url.split('.')[-1]
    return ext


def save_images(image_urls, directory):
    if not os.path.exists(directory):
        os.makedirs(directory)
    for num, image_url in enumerate(image_urls):
        image = get_content(image_url)
        ext = image_url.split('.')[-1]
        #print(ext)
        filepath = f"{directory}/hubble{num+1}.{ext}"
        save_image(image, filepath)


def get_collection_ids(collection) -> List:
    payload = {"page": "all", "collection_name": collection}
    url = 'http://hubblesite.org/api/v3/images'
    content = json.loads(get_content(url, payload))
    ids = []
    for hub in content:
        ids.append(str(hub.get('id')))
    return ids


def get_collection_urls(collection):
    collection_ids = get_collection_ids(collection)
    base_url = "http://hubblesite.org/api/v3/image/"
    dl_url = "https://hubblesite.org/uploads/image_file/image_attachment"
    collection_urls = []
    for elem in collection_ids:
        url = base_url + elem
        files = json.loads(get_content(url))
        dl = files.get("image_files")[-1].get('file_url')
        dl = "/".join(dl.split("/")[-2:])
        pic_url = dl_url+  '/' + dl
        collection_urls.append(pic_url)
    return collection_urls


def get_picture_center(image):
    center_x = int(image.width/2)
    center_y = int(image.height/2)
    return (center_x, center_y)


def get_frame_crds(image):
    crd_x, crd_y = get_picture_center(image)
    if crd_x > crd_y:
        x1 = crd_x - crd_y
        y1 = 0
        x2 = crd_x + crd_y
        y2 = crd_y * 2
    else:
        x1 = 0
        y1 = crd_y - crd_x
        x2 = crd_x * 2
        y2 = crd_x + crd_y
    return (x1, y1, x2, y2)

def crop_image(image):
    frame_coordinates = get_frame_crds(image)
    croped = image.crop(frame_coordinates)
    return croped

if __name__ == "__main__":
   #urls = get_collection_urls("spacecraft")
   #save_images(urls, 'images')
   image = Image.open("images/hubble5.png")
   croped = crop_image(image)
   croped.save("crop.jpg")
