from selenium.webdriver.common.by import By
from .base_page import BasePage
from config import BASE_URL


class LoginPage(BasePage):
    USER = (By.CSS_SELECTOR, '[data-test="username"]')
    PASSWORD = (By.CSS_SELECTOR, '[data-test="password"]')
    LOGIN = (By.CSS_SELECTOR, '[data-test="login-button"]')
    ERROR = (By.CSS_SELECTOR, '[data-test="error"]')

    def open(self):
        self.driver.get(BASE_URL)
        return self

    def login(self, username, password):
        self.visible(self.USER).send_keys(username)
        self.visible(self.PASSWORD).send_keys(password)
        self.click(self.LOGIN)
