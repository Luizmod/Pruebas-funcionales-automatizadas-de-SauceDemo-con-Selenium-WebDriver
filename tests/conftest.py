import os
from pathlib import Path
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from config import USERNAME, PASSWORD
from pages.login_page import LoginPage


@pytest.fixture
def driver(request):
    options = Options()
    if os.getenv('HEADLESS', '0') == '1':
        options.add_argument('--headless=new')
    options.add_argument('--window-size=1440,1000')
    browser = webdriver.Chrome(options=options)  # Selenium Manager gestiona el driver.
    yield browser
    # Evidencia si la prueba falla. No implica que se ejecutó exitosamente.
    report = getattr(request.node, 'rep_call', None)
    if report is not None and report.failed:
        screenshots = Path('reports/screenshots')
        screenshots.mkdir(parents=True, exist_ok=True)
        browser.save_screenshot(str(screenshots / f'{request.node.name}.png'))
    browser.quit()


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    setattr(item, f'rep_{report.when}', report)


@pytest.fixture
def logged_in(driver):
    page = LoginPage(driver).open()
    page.login(USERNAME, PASSWORD)
    from selenium.webdriver.support.ui import WebDriverWait
    WebDriverWait(driver, 12).until(lambda d: '/inventory.html' in d.current_url)
    return driver
