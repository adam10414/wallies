"""This script will gather needed inforamtion to run fresh_wallies.py"""

import os, argparse, json
import sys


def read_api_key():
    """Fetches the API key currently stored. in the user-settings dir."""

    try:
        if os.path.exists("./user-settings"):
            with open(os.path.join("user-settings", "preferences.json"),
                      "r") as preference_file:
                preferences = json.load(preference_file)

                return preferences["api_key"]

    except FileNotFoundError:
        pass


def write_api_key(key, file_path):
    with open(file_path, "w") as preference_file:
        settings = {"api_key": key}
        json.dump(settings, preference_file)


def set_api_key(input):
    """Sets the API key"""

    input = parser.parse_args()

    if input.apikey:
        write_api_key(input.apikey, os.path.join("user-settings", "preferences.json"))

    else:
        answer = ""
        print("""No API key was given as an argument when running this script.
        API keys will help this script fetch relevant wallpapers for you.
        After creating an account on wallhaven, it can be found here:
        https://wallhaven.cc/settings/account
        """)
        while answer not in ("y", "n"):
            answer = input(
                "Are you sure you would like to proceed without an API key? (y/n):"
            )

            if answer == "y":
                write_api_key(None, "./user-settings/preferences.json")

            if answer == "n":
                api_key = input("Copy and paste the API key here:")
                write_api_key(api_key, "./user-settings/preferences.json")


parser = argparse.ArgumentParser(
    formatter_class=argparse.RawDescriptionHelpFormatter,
    description='''\
    Welcome to wallies! A wallpaper app powered by https://wallhaven.cc
    After this script collects an API key from you once, it will continue using it
    for futer runs. To provide a new API key to this script, run it
    with the argument --apikey.
    
    By default, this app will store known wallies locally, but if you want you can
    store known wallies remotely using google sheets. If you want, you can do this by
    using --set-remote true and then supply another arg of
    --google-sheet https://google/sheet/url/goes/here
    
    You can disable remote storage by calling this app again with the arg
    --set-remote false''')

parser.add_argument(
    "--apikey",
    help="The API Key generated here: https://wallhaven.cc/settings/account",
)

parser.add_argument(
    "--set-remote",
    help="Tells the app whether or not to use a remote shet for storage.",
    choices=["true", "false"],
    default=False
)

known_args = parser.parse_known_args()[0]
if known_args.set_remote == "true"
    sheet_required = True

parser.add_argument(
    "--google-sheet",
    required=sheet_required,
    help="The URL of the google sheet you want wallies to use."
)

input = parser.parse_args()


def get_input():
    if read_api_key() and not input.apikey:
        input.apikey = read_api_key()

    elif input.apikey:
        write_api_key(input.apikey, os.path.join("user-settings", "preferences.json"))

    else:
        return set_api_key(input)

    return input


# TODO:
# Add a --dir arg to this script so the user can specify which dir they want to use. (Default is desktop.)
