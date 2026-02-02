# AutomationExercise UI + API Automation (Python + Pytest + Playwright)

UI automation framework for practicing end-to-end testing on: https://automationexercise.com/

## Tech Stack
- **Language:** Python
- **Test Runner:** pytest
- **Browser Automation:** Playwright (Python)
- **Test Data:** Faker
- **Config:** python-dotenv (`.env`)
- **Reporting:** Playwright HTML report (optional: Allure)

---

## Project Structure
├─ config/
│ └─ settings.py # base_url / headless settings
├─ data/
│ ├─ models.py # dataclasses for test data
│ └─ user_factory.py # Faker-based user generator
├─ pages/
│ ├─ base_page.py # base page object
│ ├─ home_page.py # home page actions/assertions
│ ├─ login_page.py # login/signup actions/assertions
│ └─ account_page.py # account page assertions
├─ tests/
│ └─ ui/
│ ├─ test_smoke_home.py
│ └─ test_signup_login.py
├─ utils/
│ └─ helpers.py # common helpers (optional)
├─ conftest.py # pytest fixtures (base_url, playwright config)
├─ pytest.ini # pytest config + markers
├─ requirements.txt
└─ README.md

---

### Setup

1)Create and activate virtual environment:
python -m venv .venv
source .venv/bin/activate
2) Install dependencies
pip install -r requirements.txt
3) Install Playwright browsers
playwright install

### Configuration

Create a .env file in the project root (or copy from .env.example):
BASE_URL=https://automationexercise.com
HEADLESS=true
BASE_URL – site under test
HEADLESS – true/false to run headless or headed

###Running Tests
Run all tests:
pytest

Run smoke tests only:
pytest -m smoke

Run with headed browser:
HEADLESS=false pytest

Run a single test file:
pytest tests/ui/test_signup_login.py

### Reporting
Option A: Playwright HTML report 
pytest --html=reports/report.html --self-contained-html


Option B: Allure 
Install:
pip install allure-pytest
Run with Allure results:
pytest --alluredir=allure-results

Generate and open report:
allure serve allure-results

###Notes / Best Practices:
Use unique emails for signup tests to avoid Email Address already exist!.
Keep stable locators (prefer data-qa, get_by_role, and visible text where stable).
Page Object Model keeps tests readable and reduces locator duplication.
For long E2E flows, mark as @pytest.mark.regression and keep smoke suite fast.