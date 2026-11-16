"""Diagnóstico adicional, separado de los seis casos y de sus resultados."""
import json
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage
from config import USERNAME, PASSWORD

options = Options()
options.add_argument('--headless=new')
options.add_argument('--window-size=1440,1000')
options.set_capability('goog:loggingPrefs', {'browser': 'ALL'})
browser = webdriver.Chrome(options=options)
try:
    login = LoginPage(browser).open()
    login.login(USERNAME, PASSWORD)
    login.wait_path('/inventory.html')
    inventory = InventoryPage(browser)
    inventory.add_backpack()
    inventory.open_cart()
    CartPage(browser).checkout()
    checkout = CheckoutPage(browser)
    browser.execute_script("window.events=[]; ['input','change','click'].forEach(t=>document.addEventListener(t,e=>window.events.push({type:t,id:e.target.id,value:e.target.value}),true))")
    for locator, value in [(checkout.FIRST_NAME, 'Prueba'), (checkout.LAST_NAME, 'Academica'), (checkout.POSTAL_CODE, '10101')]:
        field = checkout.visible(locator)
        field.send_keys(value)
        print(locator, 'value=', field.get_attribute('value'), flush=True)
    print('before continue', browser.execute_script('return window.events'), flush=True)
    try:
        from selenium.webdriver.common.action_chains import ActionChains
        ActionChains(browser).move_to_element(checkout.visible(checkout.CONTINUE)).click().perform()
        checkout.wait_path('/checkout-step-two.html')
        print('overview', browser.current_url, flush=True)
        checkout.finish()
        print('completed', checkout.text(checkout.COMPLETE_HEADER), flush=True)
    except Exception as exc:
        print(type(exc).__name__, 'url=', browser.current_url, flush=True)
    print('events', browser.execute_script('return window.events'), flush=True)
    print('console', json.dumps(browser.get_log('browser')), flush=True)
    browser.save_screenshot('reports/diagnostico_checkout.png')
finally:
    browser.quit()

