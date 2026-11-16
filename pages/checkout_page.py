from selenium.webdriver.common.by import By
from .base_page import BasePage


class CheckoutPage(BasePage):
    FIRST_NAME = (By.CSS_SELECTOR, '[data-test="firstName"]')
    LAST_NAME = (By.CSS_SELECTOR, '[data-test="lastName"]')
    POSTAL_CODE = (By.CSS_SELECTOR, '[data-test="postalCode"]')
    CONTINUE = (By.CSS_SELECTOR, '[data-test="continue"]')
    FINISH = (By.CSS_SELECTOR, '[data-test="finish"]')
    COMPLETE_HEADER = (By.CSS_SELECTOR, '[data-test="complete-header"]')

    def enter_information(self, first_name, last_name, postal_code):
        self.visible(self.FIRST_NAME).send_keys(first_name)
        self.visible(self.LAST_NAME).send_keys(last_name)
        self.visible(self.POSTAL_CODE).send_keys(postal_code)
        self.click(self.CONTINUE)
        self.wait_path('/checkout-step-two.html')

    def finish(self):
        self.click(self.FINISH)
        self.wait_path('/checkout-complete.html')
