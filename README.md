# Space Instagram

Scripts to download pics from SpaceX API and hubble API.

### How to install

Python3 should be already installed. 
Then use `pip` (or `pip3`, if there is a conflict with Python2) to install dependencies:
```
pip install -r requirements.txt
```

Add instagram login, password and picture directory name to file `.env`: <br>
`login` = %login% <br>
`password` = %password% <br>
`directory` = %directory%

### How to use

To fetch images from SpaceX and Hubble library and upload them to your Instagram profile run script:
```
python3 instagram_upload.py
```
Command line interface is also available:
```
python3 instagram_upload.py --login %login% --password %password% --directory %directory%
```
#### Functions description
Function `fetch_spacex_last_launch()` from `fetch_spacex.py` returns image urls list of last SpaceX launch.<br>
Function `fetch_hubble_urls(collection)` from `fetch_hubble.py` returns image urls list of collection from Hublle.<br>
Function `save_images(image_urls, directory)` from `tools.py` saves urls to directory.<br>
Function `crop_files_in_folder(folder_name)` from `tools.py` crops images to square format.<br>
Function `load_pics(login, password, folder_path)` from `instagram_upload.py` loads pictures to Instagram from folder with square pics.

### Project Goals

The code is written for educational purposes on online-course for web-developers [dvmn.org](https://dvmn.org/).
