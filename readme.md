# Wallies - A Wallpaper App

Welcome to Wallies! I've always wanted a light weight app that would pull in nice fresh wallpapers every day, so I made one.

This app is intended to serve as a source for rotating wallpapers, and screensaver images. (If you set your wallpaper folder and screensaver folder to the same one.)

This app will pull in wall papers from [here](https://wallhaven.cc/hot). If you have an account there, this app will use your search preferences you have saved. (Given an API key.)


## Requirements:
- Python 3.6+ installed on your machine.
- You will likely want an account on https://wallhaven.cc/, and to save some custom search settings. These will be used when the script runs and pull in wall papers of your choosing.

## Installation:
- Clone/download this repo locally.
- In a terminal window navigate to this dir and run: `pip install -r requirements.txt`
- Set this script to run every time you turn on your computer so you don't have to think about it again!


## How to use:
- Open a terminal or cmd window.
- Navigate to the dir this program is stored in.
- Run: `python3 fresh_wallies.py --apikey API_KEY_GOES_HERE`
    - Alternatively you can run `python3 fresh_wallies.py -h` to see a help message.

## Notes:
- This app will create a folder on your desktop labeled, "fresh_wallies" to store the wallpapers in.
- It will create a sub-folder here labeled, "previous_wallpapers" in case you wanted to go back to any.
- Every time the script runs, it will move all files from "fresh_wallies" to "previous_wallpapers", and then download a fresh set.
- Moving "fresh_wallies" will break the program. To specifiy a new file path, run the script with the argument --dir.
    - The new directory given to this argument will need to be an absolute filepath.