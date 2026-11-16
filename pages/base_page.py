from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from config import TIMEOUT
from urllib.parse import urlparse


class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, TIMEOUT)

    def visible(self, locator):
        element = self.wait.until(EC.visibility_of_element_located(locator))
        self._record_locator(locator)
        return element

    def click(self, locator):
        element = self.wait.until(EC.element_to_be_clickable(locator))
        self._record_locator(locator)
        element.click()

    def _record_locator(self, locator):
        if not hasattr(self.driver, 'locator_checks'):
            self.driver.locator_checks = []
        self.driver.locator_checks.append({
            'url': self.driver.current_url, 'by': locator[0],
            'selector': locator[1], 'matches': len(self.driver.find_elements(*locator)),
        })

    def wait_path(self, path):
        self.wait.until(lambda d: urlparse(d.current_url).path == path)

    def absent(self, locator):
        self.wait.until(lambda d: not d.find_elements(*locator))

    def text(self, locator):
        return self.visible(locator).text
