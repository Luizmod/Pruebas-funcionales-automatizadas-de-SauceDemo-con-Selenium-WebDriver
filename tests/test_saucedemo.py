"""Seis casos de prueba de la actividad S10. Ejecutar para obtener resultados reales."""
import pytest
from selenium.webdriver.common.by import By
from config import USERNAME, PASSWORD
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage


@pytest.mark.ui
def test_cp01_login_valido(driver):
    LoginPage(driver).open().login(USERNAME, PASSWORD)
    assert '/inventory.html' in driver.current_url
    assert InventoryPage(driver).text(InventoryPage.TITLE) == 'Products'


@pytest.mark.ui
def test_cp02_login_invalido(driver):
    page = LoginPage(driver).open()
    page.login('usuario_invalido', 'clave_invalida')
    assert 'do not match' in page.text(page.ERROR).lower()
    assert '/inventory.html' not in driver.current_url


@pytest.mark.ui
def test_cp03_ordenar_precio_ascendente(logged_in):
    page = InventoryPage(logged_in)
    page.sort_low_to_high()
    prices = page.prices()
    assert len(prices) >= 2
    assert prices == sorted(prices)


@pytest.mark.ui
def test_cp04_agregar_al_carrito(logged_in):
    inventory = InventoryPage(logged_in)
    inventory.add_backpack()
    assert inventory.text(inventory.CART_BADGE) == '1'
    inventory.open_cart()
    assert 'Sauce Labs Backpack' in CartPage(logged_in).item_names()


@pytest.mark.ui
def test_cp05_eliminar_del_carrito(logged_in):
    inventory = InventoryPage(logged_in)
    inventory.add_backpack()
    inventory.open_cart()
    cart = CartPage(logged_in)
    assert 'Sauce Labs Backpack' in cart.item_names()
    cart.remove_backpack()
    assert 'Sauce Labs Backpack' not in cart.item_names()
    assert len(logged_in.find_elements(By.CSS_SELECTOR, '[data-test="shopping-cart-badge"]')) == 0


@pytest.mark.ui
def test_cp06_completar_compra(logged_in):
    inventory = InventoryPage(logged_in)
    inventory.add_backpack()
    inventory.open_cart()
    CartPage(logged_in).checkout()
    checkout = CheckoutPage(logged_in)
    checkout.enter_information('Prueba', 'Academica', '10101')
    assert '/checkout-step-two.html' in logged_in.current_url
    checkout.finish()
    assert '/checkout-complete.html' in logged_in.current_url
    assert checkout.text(checkout.COMPLETE_HEADER) == 'Thank you for your order!'
