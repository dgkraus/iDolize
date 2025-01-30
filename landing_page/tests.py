from django.test import TestCase

import pytest
from playwright.sync_api import sync_playwright

#function to test the landing page with difference browsers. probably needs to be slightly adjusted to be able to easily navigate the whole website
@pytest.fixture(params=["chromium", "firefox", "webkit"], scope="function")
def page(request, URL=""):
    with sync_playwright() as p:
        browser_type = getattr(p, request.param)
        browser = browser_type.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()

        url_name = "http://127.0.0.1:8000/" + URL #make sure this URL is set to the landing page
        
        page.goto(url_name)
        
        yield page
        
        page.close()
        browser.close()

def test_page_title(page):
    """
    make sure that the site loads correctly and shows the correct page title using different browsers
    """
    title = page.title()

    assert title == "DK Portfolio", f"Expected 'DK Portfolio' but got '{title}' instead"

def test_landing_page_contains_idolize_link(page):
    """
    makes sure that the page shows a button with the correct link and that it is clickable
    """
    idolize_link = page.locator('a[href="/idolize/"]') #change for correct link later

    assert idolize_link.is_visible()
    assert idolize_link.is_enabled()

    idolize_link.click()
    assert page.url == "http://127.0.0.1:8000/idolize/"