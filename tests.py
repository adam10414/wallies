"""A module to test things."""
import unittest, json, os
import setup


class TestSetupMethods(unittest.TestCase):
    def setUp(self) -> None:
        with open("./test_preferences.json", "w") as test_file:
            preferences = {"api_key": "TEST"}
            json.dump(preferences, test_file)

    def test_write_api_key(self):
        with open("./test_preferences.json", "r") as test_file:
            original_value = json.load(test_file)["api_key"]

        self.assertEqual(original_value, "TEST")
        setup.write_api_key("TEST_VALUE", "./test_preferences.json")

        with open("./test_preferences.json", "r") as test_file:
            new_vaule = json.load(test_file)["api_key"]

        self.assertEqual(new_vaule, "TEST_VALUE")

    def tearDown(self):
        os.remove("./test_preferences.json")