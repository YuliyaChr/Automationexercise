import pytest
import requests
from playwright.sync_api import sync_playwright
from faker import Faker

fake = Faker()

@pytest.fixture(scope="session")
def browser():
    """Launches the browser once per session"""
    playwright = sync_playwright().start()
    browser = playwright.chromium.launch(headless=False, args=["--start-maximized"] )

    yield browser
    print("browser created")
    browser.close()
    print("browser closed")
    playwright.stop()


@pytest.fixture(scope="session")
def context(browser):
    context = browser.new_context(viewport = None)
    yield context
    print("context created")
    context.close()
    print("context closed")


def test_open_google(browser):
    page = browser.new_page()
    page.goto("https://google.com")
    assert "Google" in page.title()

@pytest.fixture
def page(context):
    """Creates a new tab (page) for each test"""
    page = context.new_page()
    yield page
    print("page created")
    page.close()
    print("page closed")


# browser() - opens browser one time per session
# page() - creates new tab(page) for each test


@pytest.fixture
def registered_user():
    url = "https://automationexercise.com/api/createAccount"

    fake_email = fake.email()
    fake_name = fake.first_name()
    password = "123qwe"
    fake_lastname = fake.last_name()

    payload = {
        "name": fake_name,
        "email": fake_email,
        "password": password,
        "title": "Mr",
        "birth_date": "2",
        "birth_month": "January",
        "birth_year": "2000",
        "newsletter": "true",
        "optin": "true",
        "firstname": fake_name,  #id = id="first_name"
        "lastname": fake_lastname,  #id="last_name"
        "company": fake.company(),
        "address1": fake.address(),
        "country": "United States",
        "state": fake.state(),
        "city": fake.city(),
        "zipcode": fake.zipcode(),
        "mobile_number": fake.phone_number()
    }

    response = requests.post(
        url=url,
        data=payload
    )
    response.raise_for_status()
    return {"email": fake_email,
            "password": password,
            "response": response,
            "first_name": fake_name,
            "last_name": fake_lastname
            }

