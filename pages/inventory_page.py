from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from .base_page import BasePage


class InventoryPage(BasePage):
    TITLE = (By.CSS_SELECTOR, '[data-test="title"]')
    SORT = (By.CSS_SELECTOR, '[data-test="product-sort-container"]')
    PRICES = (By.CSS_SELECTOR, '[data-test="inventory-item-price"]')
    ADD_BACKPACK = (By.CSS_SELECTOR, '[data-test="add-to-cart-sauce-labs-backpack"]')
    CART_BADGE = (By.CSS_SELECTOR, '[data-test="shopping-cart-badge"]')
    CART = (By.CSS_SELECTOR, '[data-test="shopping-cart-link"]')

    def sort_low_to_high(self):
        Select(self.visible(self.SORT)).select_by_value('lohi')

    def prices(self):
        self.visible(self.PRICES)
        return [float(el.text.replace('$', '').strip()) for el in self.driver.find_elements(*self.PRICES)]

    def add_backpack(self):
        self.click(self.ADD_BACKPACK)

    def open_cart(self):
        self.click(self.CART)
