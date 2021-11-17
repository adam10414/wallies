"""A module to store services for the Wallhaven API."""

import requests, csv, datetime, os, platform, time

today = datetime.date.today().isoformat()


# I did not plan this class out very well...
class Wallhaven():
    """An interface to interact with the Wallhaven API.
    See API documentation here: https://wallhaven.cc/help/api"""
    def __init__(self, api_key) -> None:
        self._search_url = "https://wallhaven.cc/api/v1/search"
        self.search_page = 1
        self._parameters = {"apikey": api_key, "sorting": "favorites"}

        if os.path.exists("./components/data/seen_wallies.csv"):
            with open("./components/data/seen_wallies.csv", "r") as csv_file:
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
        if not os.path.exists(f"{self.desktop}/wallies"):
            os.mkdir(f"{self.desktop}/wallies")

        # Creating an archive folder so data is not lost.
        if not os.path.exists(f"{self.desktop}/wallies/archive"):
            os.mkdir(f"{self.desktop}/wallies/archive")

        # Moving the current set of files to the archive folder.
        file_list = os.listdir(f"{self.desktop}/wallies")
        file_list.remove("archive")

        if len(file_list) > 0:
            for file in file_list:
                os.replace(f"{self.desktop}/wallies/{file}",
                           f"{self.desktop}/wallies/archive/{file}")

    def get_raw_search_results(self, search_page):
        parameters = self._parameters.copy()
        parameters["page"] = search_page
        return requests.get(self._search_url, params=parameters)

    def get_search_result_data(self, search_page):

        parameters = self._parameters.copy()
        parameters["page"] = search_page

        return requests.get(self._search_url, params=parameters).json()["data"]

    def get_wallpaper_paths(self, search_data):
        """Downloads the specified number of wallpapers.
        search_data: - List returned by self.get_search_result_data"""

        return [wallie["path"] for wallie in search_data]

    def get_ids(self, search_data):
        """Returns a list of IDs from the given search data."""

        return [wallie["id"] for wallie in search_data]

    def update_seen_wallies_csv(self, id_list):
        """Updates the wallies csv with a list of IDs and when they were seen.
        id_list: list - ids of wallpapers."""

        todays_seen_wallies = [{
            "id": id,
            "seen_on": today
        } for id in id_list if id not in self.seen_wallie_ids
                               ] + self._seen_wallie_data

        # Creating the file if it doesn't already exist.
        if not os.path.exists("./components/data/seen_wallies.csv"):
            with open("./components/data/seen_wallies.csv", "w") as csv_file:
                writer = csv.DictWriter(csv_file, fieldnames=["id", "seen_on"])
                writer.writeheader()
                for wallie in todays_seen_wallies:
                    writer.writerow(wallie)

        # If it does already exist, then just add rows to it.
        if os.path.exists("./components/data/seen_wallies.csv"):
            with open("./components/data/seen_wallies.csv", "w") as csv_file:
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

        with open(f"{self.desktop}/wallies/{file_name}{file_extension}",
                  "wb") as image_file:
            image_file.write(wallie_response._content)
        print(f"Downloaded wallie: {file_name}!")

    def get_new_wallies(self, ammount_of_wallies):
        """Returns new wallies that this app has not seen before.
        ammount_of_wallies: int - not to exceed 15"""

        new_wallies = []
        search_page = 1

        while len(new_wallies) < ammount_of_wallies:
            print(f"Searching page {search_page}")
            response = self.get_raw_search_results(search_page)

            print(f"""
            Satus: {response.status_code}
            """)

            # For some reason their rate limits for search pages are different
            # than what they have documented, and it does not line up with the
            # rate limit left over in the headers.
            if response.status_code == 429:
                time.sleep(2)

            elif response.status_code in range(200, 300):
                search_data = response.json()["data"]

                for wallie in search_data:
                    if wallie["id"] not in self.seen_wallie_ids and len(
                            new_wallies) < ammount_of_wallies:
                        new_wallies.append(wallie)

                search_page += 1

        return new_wallies