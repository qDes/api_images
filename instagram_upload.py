import configargparse
import os
import glob

from instabot import Bot
from time import sleep
from tools import crop_files_in_folder
from tools import get_posted_pics
from tools import save_images
from fetch_spacex import fetch_spacex_last_launch
from fetch_hubble import fetch_hubble_urls


def upload_pics(login, password, folder_path):
    bot = Bot()
    bot.login(username=login, password=password)
    timeout = 30
    posted_pic_list = get_posted_pics()
    pics = glob.glob(folder_path + "/*.*")
    for pic in pics:
        bot.upload_photo(pic)
        if bot.api.last_response.status_code != 200:
            break
        if pic not in posted_pic_list:
            posted_pic_list.append(pic)
            with open("pics.txt", "a", encoding="utf8") as f:
                f.write(pic + "\n")
        sleep(timeout)


if __name__ == "__main__":
    parser = configargparse.ArgParser(description='instagram pic uploader',
                                      default_config_files=['.env'])
    parser.add("--login", help="instagram login")
    parser.add("--password", help="instagram password")
    parser.add("--directory", help="directory with images")
    args = parser.parse_args()
    login, password, directory = args.login, args.password, args.directory
    if not os.path.exists(directory):
        fetched_images = fetch_spacex_last_launch()
        fetched_images += fetch_hubble_urls()
        save_images(fetched_images, directory)
        crop_files_in_folder(directory)
    upload_pics(login, password, "./{directory}/cropped")
