"""This script will fetch the hot wallpapers from https://wallhaven.cc/hot"""

import platform, os

from components.wallhaven import Wallhaven

from setup import get_api_key

api_key = get_api_key()

wallhaven = Wallhaven(api_key)

# Crawling each page and collecting wallies we have not seen yet.
new_wallies = wallhaven.get_new_wallies(15)
todays_wallie_ids = [wallie["id"] for wallie in new_wallies]

wallhaven.update_seen_wallies_csv(todays_wallie_ids)

# Downloading each image:
for wallie in new_wallies:
    wallhaven.download_iamge(wallie)