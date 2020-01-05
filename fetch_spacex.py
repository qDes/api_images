import json

from tools import get_response
from typing import List


def fetch_spacex_last_launch() -> List:
    url = 'https://api.spacexdata.com/v3/launches/'
    launches = get_response(url).json()[::-1]
    for launch in launches:
        images = launch.get("links").get("flickr_images")
        if images:
            break
    return images
