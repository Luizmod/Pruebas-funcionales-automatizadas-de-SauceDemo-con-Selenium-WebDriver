"""Seis casos de prueba de la actividad S10. Ejecutar para obtener resultados reales."""
import pytest
from urllib.parse import urlparse
from config import USERNAME, PASSWORD
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage


@pytest.mark.ui
def test_cp01_login_valido(driver, observed):
    login = LoginPage(driver).open()
    login.login(USERNAME, PASSWORD)
    login.wait_path('/inventory.html')
    observed.update(path=urlparse(driver.current_url).path,
                    title=InventoryPage(driver).text(InventoryPage.TITLE))
    assert observed['path'] == '/inventory.html'
    assert observed['title'] == 'Products'


@pytest.mark.ui
def test_cp02_login_invalido(driver, observed):
    page = LoginPage(driver).open()
    page.login('usuario_invalido', 'clave_invalida')
    observed.update(error=page.text(page.ERROR), path=urlparse(driver.current_url).path)
    assert observed['error'] == 'Epic sadface: Username and password do not match any user in this service'
    assert observed['path'] == '/'


@pytest.mark.ui
def test_cp03_ordenar_precio_ascendente(logged_in, observed):
    page = InventoryPage(logged_in)
    page.sort_low_to_high()
    prices = page.prices()
    observed['prices'] = [str(price) for price in prices]
    assert len(prices) >= 2
    assert prices == sorted(prices)


@pytest.mark.ui
def test_cp04_agregar_al_carrito(logged_in, observed):
    inventory = InventoryPage(logged_in)
    inventory.add_backpack()
    observed['badge'] = inventory.text(inventory.CART_BADGE)
    assert observed['badge'] == '1'
    inventory.open_cart()
    cart = CartPage(logged_in)
    cart.visible(cart.ITEM_NAMES)
    observed['items'] = cart.item_names()
    assert observed['items'] == ['Sauce Labs Backpack']


@pytest.mark.ui
def test_cp05_eliminar_del_carrito(logged_in, observed):
    inventory = InventoryPage(logged_in)
    inventory.add_backpack()
    inventory.open_cart()
    cart = CartPage(logged_in)
    cart.visible(cart.ITEM_NAMES)
    observed['before'] = cart.item_names()
    assert observed['before'] == ['Sauce Labs Backpack']
    cart.remove_backpack()
    cart.absent(inventory.CART_BADGE)
    observed.update(after=cart.item_names(), badge_count=len(logged_in.find_elements(*inventory.CART_BADGE)))
    assert observed['after'] == []
    assert observed['badge_count'] == 0


@pytest.mark.ui
def test_cp06_completar_compra(logged_in, observed):
    inventory = InventoryPage(logged_in)
    inventory.add_backpack()
    inventory.open_cart()
    CartPage(logged_in).checkout()
    checkout = CheckoutPage(logged_in)
    checkout.enter_information('Prueba', 'Academica', '10101')
    observed['overview_path'] = urlparse(logged_in.current_url).path
    assert observed['overview_path'] == '/checkout-step-two.html'
    checkout.finish()
    observed.update(path=urlparse(logged_in.current_url).path,
                    message=checkout.text(checkout.COMPLETE_HEADER))
    assert observed['path'] == '/checkout-complete.html'
    assert observed['message'] == 'Thank you for your order!'
