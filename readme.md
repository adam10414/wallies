# Wallies - A Wallpaper App

Welcome to Wallies! I've always wanted a light weight app that would pull in nice fresh wallpapers every day, so I made one.

This app is intended to serve as a source for rotating wallpapers, and screensaver images. (If you set your wallpaper folder and screensaver folder to the same one.)

This app will pull in wall papers from [here](https://wallhaven.cc/toplist). If you have an account there, this app will use your search preferences you have saved. (Given an API key.)


## Requirements:
- [Python 3.6+](https://www.python.org/downloads/) installed on your machine.
- You will likely want an account on https://wallhaven.cc/, and to save some custom search settings. These will be used when the script runs and pull in wall papers of your choosing.

## Installation:
- Clone/download this repo locally.
- In a terminal window navigate to this dir and run: `pip install -r requirements.txt`
- Run the program independently at least once, see "How to use" section below.
- (Recommended) (See Notes below) It's recommended to set your computer to rotate the wallpaper once every hour, and to set the wallpaper source folder to the folder this script produces on your desktop. If you see your desktop once / hour, it will last you 15 hours before it loops back again.
- (Recommended) Set this script to run every time you turn on your computer so you don't have to think about it again!
    - Windows:
        1. See [this page](https://www.windowscentral.com/how-create-automated-task-using-task-scheduler-windows-10) for tips on scheduling this to run every day.

    - MacOS: (Sorry for the long conveluted instructions. If you know a better way, please open an issue to bring it to my attention.)
        1. Find the directory of this script.
        2. Right click and open job.sh with the text editor of your choice.
        3. Insert a line between `\#!/bin/sh` and `python3 fresh_wallies.py` and type in this relative path: `cd file/path/to/this/script/on/your/computer/`
        4. Open a terminal window, and navigate to the directory of this script.
        5. Type `sudo chmod u+x job.sh`.
        6. Enter your password.
        7. Click the Apple in the top left corner > System Preferences > Users & Groups > Click your profile > Login Items
        8. Click the lock on the bottom left corner, and ensure it's unlocked. (You may need to enter your password.)
        9. Click the + symbol > find the directory where this script lives.
        10. Double click job.sh. (Or just single click it and then click Add.)


## How to use:
- Open a terminal or cmd window.
- Navigate to the dir this program is stored in.
- Run: `python3 fresh_wallies.py --apikey API_KEY_GOES_HERE`
    - Alternatively you can run `python3 fresh_wallies.py -h` to see a help message.

## Notes:
- This app will create a folder on your desktop labeled, "wallies" to store the wallpapers in.
    - If you already have a folder named wallies, then it will archive your current wallpapers. See next note.
- It will create a sub-folder here labeled, "archive" in case you wanted to go back to any.
- Every time the script runs, it will move all files from "wallies" to "archive", and then download a fresh set.