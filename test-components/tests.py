import unittest

from components.wallhaven import Wallhaven
from setup import get_api_key


class TestWallhaven(unittest.TestCase):
    def test_get_wallpaper_paths(self):
        self.api_key = get_api_key
        self.wallhaven = Wallhaven(self.api_key)
        search_results = [{"path": "testpath1"}, {"path": "testpath2"}]
        path_list = self.wallhaven.get_wallpaper_paths(search_results, 2)
        path_length = len(path_list)

        self.assertEqual(path_length, 2)
        self.assertEqual(path_list[0], "testpath1")
        self.assertEqual(path_list[1], "testpath2")

        new_results = [{"path": "testpath3"}, {"path": "testpath4"}]
        all_results = search_results + new_results
