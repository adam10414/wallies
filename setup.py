"""This script will gather needed inforamtion to run fresh_wallies.py"""

import os, argparse, json


def read_api_key():
    """Fetches the API key currently stored. in the user-settings dir."""

    try:
        if os.path.exists("./user-settings"):
            with open("./user-settings/preferences.json",
                      "r") as preference_file:
                preferences = json.load(preference_file)

                return preferences["api_key"]

    except FileNotFoundError:
        pass


def write_api_key(key, file_path):
    with open(file_path, "w") as preference_file:
        settings = {"api_key": key}
        json.dump(settings, preference_file)


def set_api_key():
    """Sets the API key"""

    args = parser.parse_args()

    if args.apikey:
        write_api_key(args.apikey, "./user-settings/preferences.json")
        return args.apikey

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
                return api_key


parser = argparse.ArgumentParser(
    formatter_class=argparse.RawDescriptionHelpFormatter,
    description='''\
    Welcome to wallies! A wallpaper app powered by https://wallhaven.cc
    After this script collects an API key from you once, it will continue using it
    for futer runs. To provide a new API key to this script, run it
    with the argument --apikey.''')

parser.add_argument(
    "--apikey",
    help="The API Key generated here: https://wallhaven.cc/settings/account",
)

args = parser.parse_args()


def get_api_key():
    if read_api_key() and not args.apikey:
        return read_api_key()

    elif args.apikey:
        write_api_key(args.apikey, "./user-settings/preferences.json")
        return args.apikey

    else:
        return set_api_key()


# TODO:
# Add a --dir arg to this script so the user can specify which dir they want to use. (Default is desktop.)
