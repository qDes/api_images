import requests


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


if __name__ == "__main__":
    filename = "hubble.jpg"
    url = "https://upload.wikimedia.org/wikipedia/commons/3/3f/HST-SM4.jpeg"
    picture = get_content(url)
    with open(filename, "wb") as f:
        f.write(picture)
