from time import sleep
import re
from selenium.common.exceptions import NoSuchElementException

login = ''
password = r'7acA3L2K4rEii3XU599mhs74Mg6LZ9BAz84k72zL2L' \
           'mp3X9U7r36fn6HYrE62A8ZaJk83i2c2Ry7Z5JzikScX' \
           '5B584nT695MiZ6a8h43FxSdV6N9g3Fz9aF3y3GCc778D' \
           'did52XC9t3B7Z56k6KgSsMFt9zs7Z67j3gB344gPK3' \
           'J4j9agS5KgLX4255NriaXL32p3E5a'


def authorization_fb(driver, login_facebook=login, pass_facebook=password, new_page=True, delay=0.1):
    """Авторизація у фейсбук
    authorization_fb -> driver
    @login_facebook
    @pass_facebook
    @new_page -> this trick doesn't work
    @delay
    """
    try:
        if new_page:
            # це не раюотає
            window_after = driver.window_handles[1]
            driver.switch_to.window(window_after)

        driver.get(r'https://www.facebook.com/')
        id_enter = re.search('u_0_d_..', driver.page_source).group()
        sleep(delay)
        driver.find_element_by_id('email').send_keys(login_facebook)
        sleep(delay)
        driver.find_element_by_id('pass').send_keys(pass_facebook)
        sleep(delay)
        driver.find_element_by_id(id_enter).click()
        sleep(delay)

        # попитки зайти
        for i in range(1000):
            try:
                driver.find_element_by_id('pass')
                sleep(0.01)
            except NoSuchElementException:
                print('Авторизація виконана')
                return driver
        print('час авторицації минув')
    except:
        print('Ошибка авторизации')
    return driver

