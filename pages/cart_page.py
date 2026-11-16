from selenium.webdriver.common.by import By
from .base_page import BasePage


class CartPage(BasePage):
    ITEM_NAMES = (By.CSS_SELECTOR, '[data-test="inventory-item-name"]')
    REMOVE_BACKPACK = (By.CSS_SELECTOR, '[data-test="remove-sauce-labs-backpack"]')
    CHECKOUT = (By.CSS_SELECTOR, '[data-test="checkout"]')

    def item_names(self):
        self.wait_path('/cart.html')
        return [item.text for item in self.driver.find_elements(*self.ITEM_NAMES)]

    def remove_backpack(self):
        self.click(self.REMOVE_BACKPACK)
        self.absent(self.REMOVE_BACKPACK)

    def checkout(self):
        self.click(self.CHECKOUT)
        self.wait_path('/checkout-step-one.html')
