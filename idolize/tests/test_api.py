from django.test import TestCase

import pytest
from playwright.sync_api import sync_playwright, expect
from asgiref.sync import sync_to_async

from idolize.models import IdolDatabase
from idolize.serializers import IdolSerializer
from idolize.tests.test_database import set_up_db_entries

@pytest.fixture(params=["chromium", "firefox", "webkit"], scope="function")
def page(request, URL=""):
    with sync_playwright() as p:
        browser_type = getattr(p, request.param)
        browser = browser_type.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()

        url_name = "http://127.0.0.1:8000/idolize/api/"
            
        page.goto(url_name)
            
        yield page
            
        page.close()
        browser.close()

@pytest.fixture(scope="function")
def db_setup():
    """
    setup a mock database to use in tests
    """
    set_up_db_entries()
    yield

class TestAPI():
    @pytest.mark.django_db
    def test_api_response(self, db_setup):
        """
        after setting up the database, the serializer should return the correct number of API responses
        """

        db_entries = IdolDatabase.objects.all()
        serializer = IdolSerializer(db_entries, many=True)
        api_response = serializer.data
        assert len(api_response) == 2, f"The API response didn't return 2 responses as expect, it returned {api_response}"

    @pytest.mark.django_db
    def test_api_is_visible(self, page):
        """
        when navigating to the appropriate URL, the correctly formatted API information should be visible in the browser
        """

        locator = page.locator("text=HTTP 200 OK")

        expect(locator).to_be_visible()



