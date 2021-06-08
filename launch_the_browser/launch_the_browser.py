from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# ------------------------------ SETTINGS --------------------------------------
# шлях до драйвера хром
chrome_link = './chromedriver.exe'


def browser_settings() -> 'object':
    """ Вимкнення спливаючих вікон, запуск браузера
    browser_settings() -> driver """
    option = Options()

    option.add_argument("--disable-infobars")
    option.add_argument("start-maximized")
    option.add_argument("--disable-extensions")

    # Pass the argument 1 to allow and 2 to block
    option.add_experimental_option("prefs", {
        "profile.default_content_setting_values.notifications": 1
    })
    return webdriver.Chrome(chrome_options=option, executable_path=chrome_link)

