import requests
import os

from PIL import Image


def get_content(url, payload={}):
    try:
        cafile = 'cacert.pem'  # http://curl.haxx.se/ca/cacert.pem
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


def get_extension(url):
    ext = url.split('.')[-1]
    return ext


def save_images(image_urls, directory):
    if not os.path.exists(directory):
        os.makedirs(directory)
    for num, image_url in enumerate(image_urls):
        image = get_content(image_url)
        ext = image_url.split('.')[-1]
        filepath = f"{directory}/hubble{num+1}.{ext}"
        save_image(image, filepath)


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
    cropped = image.crop(frame_coordinates)
    return cropped


def crop_files_in_folder(folder_name):
    pictures = os.listdir(folder_name)
    if not os.path.exists(f"{folder_name}/cropped"):
        os.makedirs(f"{folder_name}/cropped")
    for picture in pictures:
        try:
            image = Image.open(f"{folder_name}/{picture}")
            cropped = crop_image(image)
            cropped.save(f"{folder_name}/cropped/cropped_{picture}")
        except IOError:
            pass


def get_posted_pics():
    posted_pic_list = []
    try:
        with open("pics.txt", "r", encoding="utf8") as f:
            posted_pic_list = f.read().splitlines()
    except Exception:
        posted_pic_list = []
    return posted_pic_list
