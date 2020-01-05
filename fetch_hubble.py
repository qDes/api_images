import json

from typing import List
from tools import get_content


def get_collection_ids(collection) -> List:
    payload = {"page": "all", "collection_name": collection}
    url = 'http://hubblesite.org/api/v3/images'
    content = get_content(url, payload)
    ids = []
    for hub in content:
        id_ = hub.get('id')
        if id_:
            ids.append(str(id_))
    return ids


def fetch_hubble_urls(collection='spacecraft'):
    '''Hubble collection names
        holiday_cards, wallpaper, news, printshop,
        stsci_gallery, spacecraft, stsci_gallery
        spacecraft is deault value'''
    collection_ids = get_collection_ids(collection)
    base_url = "http://hubblesite.org/api/v3/image/"
    dl_url = "https://hubblesite.org/uploads/image_file/image_attachment"
    collection_urls = []
    for elem in collection_ids:
        url = base_url + elem
        files = get_content(url)
        dl = files.get("image_files")[-1].get('file_url')
        dl = "/".join(dl.split("/")[-2:])
        pic_url = dl_url + '/' + dl
        collection_urls.append(pic_url)
    return collection_urls
