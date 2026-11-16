import os

BASE_URL = os.getenv("SAUCEDEMO_URL", "https://www.saucedemo.com/")
USERNAME = os.getenv("SAUCEDEMO_USERNAME", "standard_user")
PASSWORD = os.getenv("SAUCEDEMO_PASSWORD", "secret_sauce")
TIMEOUT = int(os.getenv("SELENIUM_TIMEOUT", "12"))
