import pytest
from playwright.sync_api import Browser

@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    return {
        **browser_context_args,
        "base_url": "https://cerulean-praline-8e5aa6.netlify.app/",
        "viewport": {"width": 1920, "height": 1080},
    }

@pytest.fixture(scope="function")
def mobile_page(browser: Browser):
    context = browser.new_context(
        viewport={'width': 412, 'height': 915},
        user_agent="Mozilla/5.0 (Linux; Android 13; RMX3771) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Mobile Safari/537.36",
        has_touch=True,
        is_mobile=True
    )
    page = context.new_page()
    yield page
    context.close()
