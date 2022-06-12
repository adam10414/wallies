"""A module to store services for the Wallhaven API."""

import requests, csv, datetime, os, platform, time, sys

today = datetime.date.today().isoformat()

# Determining which way the slash leans based on OS. Because fuck windows.
if platform.system() == "Darwin":
    dir_char = "/"

if platform.system() == "Windows":
    dir_char = '\\'


# I did not plan this class out very well...
class Wallhaven():
    """An interface to interact with the Wallhaven API.
    See API documentation here: https://wallhaven.cc/help/api"""
    def __init__(self, api_key) -> None:
        self._search_url = "https://wallhaven.cc/api/v1/search"
        self.search_page = 1
        self._parameters = {
                            "apikey": api_key,
                            "sorting": "toplist",
                            "ratios": "16x9"}

        # This API is ratelmited to 45 requests / minute.
        self._rate_limit_remaining = 45

        if os.path.exists("."+dir_char+"components"+dir_char+"data"+dir_char+"seen_wallies.csv"):
            with open("."+dir_char+"components"+dir_char+"data"+dir_char+"seen_wallies.csv", "r") as csv_file:
                csv_reader = csv.DictReader(csv_file)

                self._seen_wallie_data = [row for row in csv_reader]
                self.seen_wallie_ids = [
                    wallie["id"] for wallie in self._seen_wallie_data
                ]
        else:
            self._seen_wallie_data = []
            self.seen_wallie_ids = []

        # Prepping file path to download images to...
        if platform.system() == "Darwin":
            self.desktop = os.path.join(os.path.join(os.path.expanduser('~')),
                                        'desktop')

        if platform.system() == "Windows":
            self.desktop = os.path.join(
                os.path.join(os.environ['USERPROFILE']), 'desktop')

        # Creating the wallies folder, or using the one that's already there.
        if not os.path.exists(f"{self.desktop}"+dir_char+"wallies"):
            os.mkdir(f"{self.desktop}"+dir_char+"wallies")

        # Creating an archive folder so data is not lost.
        if not os.path.exists(f"{self.desktop}"+dir_char+"wallies"+dir_char+"archive"):
            os.mkdir(f"{self.desktop}"+dir_char+"wallies"+dir_char+"archive")

        # Moving the current set of files to the archive folder.
        file_list = os.listdir(f"{self.desktop}"+dir_char+"wallies")
        if "archive" in file_list:
            file_list.remove("archive")

        if len(file_list) > 0:
            for file in file_list:
                os.replace(f"{self.desktop}"+dir_char+"wallies"+dir_char+f"{file}",
                           f"{self.desktop}"+dir_char+"wallies"+dir_char+"archive"+dir_char+f"{file}")

    def get_raw_search_results(self, search_page):
        parameters = self._parameters.copy()
        parameters["page"] = search_page
        response = requests.get(self._search_url, params=parameters)
        self._rate_limit_remaining = int(
            response.headers["X-RateLimit-Remaining"])
        return response

    def get_wallpaper_paths(self, search_data):
        """Downloads the specified number of wallpapers.
        search_data: - List returned by self.get_search_result_data"""

        return [wallie["path"] for wallie in search_data]

    def update_seen_wallies_csv(self, id_list):
        """Updates the wallies csv with a list of IDs and when they were seen.
        id_list: list - ids of wallpapers."""

        todays_seen_wallies = [{
            "id": id,
            "seen_on": today
        } for id in id_list if id not in self.seen_wallie_ids
                               ] + self._seen_wallie_data

        # Creating the file if it doesn't already exist.
        if not os.path.exists("."+dir_char+"components"+dir_char+"data"+dir_char+"seen_wallies.csv"):
            os.mkdir("."+dir_char+"components"+dir_char+"data")
            
            with open("."+dir_char+"components"+dir_char+"data"+dir_char+"seen_wallies.csv", "w") as csv_file:
                writer = csv.DictWriter(csv_file, fieldnames=["id", "seen_on"])
                writer.writeheader()
                for wallie in todays_seen_wallies:
                    writer.writerow(wallie)

        # If it does already exist, then just add rows to it.
        if os.path.exists("."+dir_char+"components"+dir_char+"data"+dir_char+"seen_wallies.csv"):
            with open("."+dir_char+"components"+dir_char+"data"+dir_char+"seen_wallies.csv", "w") as csv_file:
                writer = csv.DictWriter(csv_file, fieldnames=["id", "seen_on"])
                writer.writeheader()
                for wallie in todays_seen_wallies:
                    writer.writerow(wallie)

    def download_iamge(self, wallie):
        """Downloads a wallie to disk.
        wallie: dict - wallpaper from Wallhaven."""

        file_extension = wallie["path"][-4:]
        file_name = wallie["id"]
        wallie_response = requests.get(wallie["path"], params=self._parameters)

        # If fetching the wallie doesn't go well.
        while wallie_response.status_code not in range(200, 300):
            print(
                f"Could not fetch wallie {wallie['id']}, trying again in 1 second."
            )
            time.sleep(1)

            wallie_response = requests.get(wallie["path"],
                                           params=self._parameters)

        with open(f"{self.desktop}"+dir_char+"wallies"+dir_char+f"{file_name}{file_extension}",
                  "wb") as image_file:
            image_file.write(wallie_response._content)
            print(f"Downloaded wallie: {file_name}!")

    def get_new_wallies(self, ammount_of_wallies):
        """Returns new wallies that this app has not seen before. Will also handle
        rate limiting depending on the amount of wallies you want to fetch.
        ammount_of_wallies:int - cannot exceed 44."""

        new_wallies = []
        search_page = 1

        while len(new_wallies) < ammount_of_wallies:

            # Setting this inside the loop so the timer will self adjust.
            sleep_time = (60 /
                          (self._rate_limit_remaining - ammount_of_wallies))

            print(f"Searching page {search_page}")
            response = self.get_raw_search_results(search_page)

            print(f"""
            Satus: {response.status_code}
            """)

            if response.status_code in range(200, 300):
                search_data = response.json()["data"]

                for wallie in search_data:
                    if wallie["id"] not in self.seen_wallie_ids and len(
                            new_wallies) < ammount_of_wallies:
                        new_wallies.append(wallie)

                search_page += 1

                print(f"Sleeping for {sleep_time} seconds...")
                time.sleep(sleep_time)

            else:
                print(f"Response Status: {response.status_code}")
                print(f"_rate_limit_remaining: {self._rate_limit_remaining}")
                print(
                    f"Response rate limit remaining: {response.headers['X-RateLimit-Remaining']}"
                )

        return new_wallies