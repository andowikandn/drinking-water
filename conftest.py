import pytest
from playwright.sync_api import sync_playwright

@pytest.fixture(scope="function")
def browser():
    with sync_playwright() as p:
        browser = p.firefox.launch(headless=True)
        context = browser.new_context() # (viewport = { "width": 1920, "height": 1080 })
        page = context.new_page()
        page.goto('https://demoqa.com/automation-practice-form',
                   wait_until="domcontentloaded")
        yield page
        context.close()
        browser.close()