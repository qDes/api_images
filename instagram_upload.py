import os
import glob

from dotenv import load_dotenv
from instabot import Bot
from time import sleep
from tools import get_posted_pics
from tools import save_images
from fetch_spacex import fetch_spacex_last_launch
from fetch_hubble import fetch_hubble_urls


def upload_pics(login, password, folder_path):
    bot = Bot()
    bot.login(username=login, password=password)
    timeout = 30  # set timeout between posts
    posted_pic_list = get_posted_pics()
    pics = glob.glob(folder_path + "/*.*")
    for pic in pics:
        bot.upload_photo(pic)
        if bot.api.last_response.status_code != 200:
            print(bot.api.last_response)
            # snd msg
            break
        if pic not in posted_pic_list:
            posted_pic_list.append(pic)
            with open("pics.txt", "a", encoding="utf8") as f:
                f.write(pic + "\n")
        sleep(timeout)


if __name__ == "__main__":
    load_dotenv()
    login = os.environ["login"]
    password = os.environ["password"]
    upload_pics(login, password, "./images/cropped")
