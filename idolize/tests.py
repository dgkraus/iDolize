from django.test import TestCase, Client

import pytest
import requests
import re

from idolize.models import IdolDatabase
from idolize.views import idol_search

class TestCalls(TestCase):
    def set_up_db_entries(self, create_extra=0):
        """
        create test data for tests to use
        """
        IdolDatabase.objects.create(
            idol_name = "Matsumoto Karen",
            zodiac = "fake",
            height = "fake",
            birthplace = "fake"
        )
        IdolDatabase.objects.create(
            idol_name = "Test Object",
            zodiac = "Testiest",
            height = "300",
            birthplace = "Pythonland"
        )

        if create_extra != 0:
            for i in range(create_extra):
                IdolDatabase.objects.create(
                    idol_name = ("Idol_"+str(i)),
                    zodiac = "fakies",
                    height = "300",
                    birthplace = "Mars"
                )
    def test_no_match(self):
        """
        this test makes a search were 0 parameters match any db entries, which should trigger the fake_result variable in the view and show a special result
        """
        self.set_up_db_entries()

        c = Client(SERVER_NAME="localhost")
        post_data = {
            "your_zodiac": "Unknown",
            "your_height": "0",
            "your_birthplace": "Moon"
        }
        response = c.post("/idolize/", post_data)

        self.assertIn("Karen is there for you!", response.content.decode(), "Expected 'Karen' in response but didn't get")

    def test_exactly_one_match(self):
        """
        given 3 parameters that fit exactly one db entry, this should always return one predictable result based on current db entries
        """
        self.set_up_db_entries(create_extra=1)

        c = Client(SERVER_NAME="localhost")
        post_data = {
            "your_zodiac": "Testiest",
            "your_height": "300", #even if some parameters match multiple db entries, these should not show in the results if there is a closer match
            "your_birthplace": "Pythonland"
        }
        response = c.post("/idolize/", post_data)
        content = response.content.decode()

        match_count = re.findall("<strong>Idol Name:</strong>", content)

        self.assertEqual(len(match_count), 1, "there should be exactly 1 match, but there are multiple")

    def test_many_displays(self):
        """
        using parameters that give a high amount of results, all the results should still be sent in the response
        """

        self.set_up_db_entries(create_extra=100)

        c = Client(SERVER_NAME="localhost")
        post_data = {
            "your_zodiac": "Testiest",
            "your_height": "300",
            "your_birthplace": "Mars"
        }
        response = c.post("/idolize/", post_data)
        content = response.content.decode()

        match_count = re.findall("<strong>Idol Name:</strong>", content)

        self.assertEqual(len(match_count), 101, "there should be exactly 1 match, but there are multiple")


    def test_invalid_entry(self):
        """
        unusual or invalid search terms should either throw an error which may need to be handled by the view, or they should correctly fall back to the fake_result
        """
        self.set_up_db_entries()

        c = Client(SERVER_NAME="localhost")
        post_data = {
            "your_zodiac": "",
            "your_height": "",
            "your_birthplace": ""
        }
        response = c.post("/idolize/", post_data)

        self.assertIn("Karen is there for you!", response.content.decode(), "Expected 'Karen' in response but didn't get")