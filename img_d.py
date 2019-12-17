import requests
import os
import json


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


def save_image(image, path):
    if not os.path.exists(directory):
        os.makedirs(directory)
    with open(file_path, "wb") as f:
        f.write(picture)


if __name__ == "__main__":
    #directory = "images"
    #filename = "hubble.jpg"
    #url = "https://upload.wikimedia.org/wikipedia/commons/3/3f/HST-SM4.jpeg"
    #picture = get_content(url)
    #file_path = directory + "/" + filename
    #save_image(picture, file_path)
    url = 'https://api.spacexdata.com/v3/launches/'
    launches = json.loads(get_content(url))[::-1]
    for launch in launches:
        images = launch.get("links").get("flickr_images")
        if images:
            print(images)
            break
