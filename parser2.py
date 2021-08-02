from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from time import sleep
import re
import random
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys

# НАСТРОЙКИ
# шлях до драйвера хром

chrome_link = './chromedriver.exe'
# шлях до запросу
# url = 'https://www.facebook.com/search/pages?q=restaurant&filters=eyJmaWx0ZXJfcGFnZXNfbG9jYXRpb246MCI6IntcIm5hbWVcIjpcImZpbHRlcl9wYWdlc19sb2NhdGlvblwiLFwiYXJnc1wiOlwiMTAyMTQ2NjYzMTYwODMxXCJ9In0%3D'
url = 'https://www.facebook.com/search/pages?q=cafe&filters=eyJmaWx0ZXJfcGFnZXNfbG9jYXRpb246MCI6IntcIm5hbWVcIjpcImZpbHRlcl9wYWdlc19sb2NhdGlvblwiLFwiYXJnc1wiOlwiMTE2MTkwNDExNzI0OTc1XCJ9In0%3D'
# акунт фейсбук
login_facebook = ''
pass_facebook = ''
# скільки сторінок потрібно знайти
how_many_pages_to_find = 1200
how_max_like = 100
write_on_file = 1  # для записів сторінок у файл 1
name_file = r'./res_1.txt'

'''
                ЯК ПРАЦЮЄ ПРОГРАМА
    browser_settings -> виконує налаштування і запуск двигуна браузера
    auth_fb -> проходить авторизацію у фейсбук
    get_html -> переходимо по url з налаштувань, скачуємо сторінку
    processing_html -> збирає ім'я та силку на профіль у список словників list_page
    go_to_page -> переходе на сторінку зі списку та викликає get_all_information і get_date_logotype
    get_all_information -> збирає всю інформацію крім дати фото
    get_date_logotype -> шукає останнє фото, та дістає дату

'''


def browser_settings():
    '''Вимкнення спливаючих вікон, запуск браузера'''
    option = Options()

    option.add_argument("--disable-infobars")
    option.add_argument("start-maximized")
    option.add_argument("--disable-extensions")

    # Pass the argument 1 to allow and 2 to block
    option.add_experimental_option("prefs", {
        "profile.default_content_setting_values.notifications": 1
    })
    global driver
    driver = webdriver.Chrome(chrome_options=option, executable_path=chrome_link)


def auth_fb():
    '''Авторизація у фейсбук'''
    try:
        # driver.get(r'http://www.google.com/');
        driver.get('https://www.facebook.com/')
        id_enter = re.search('u_0_d_..', driver.page_source).group()
        sleep(1 + random.random())
        driver.find_element_by_id('email').send_keys(login_facebook)
        sleep(1 + random.random())
        driver.find_element_by_id('pass').send_keys(pass_facebook)
        sleep(1 + random.random())
        driver.find_element_by_id(id_enter).click()
        sleep(random.random())

        # if driver.find_element_by_id('pass'):
        #     raise Exception('Ошибка авторизации')

        print('Авторизація виконана')
    except Exception:
        print('Ошибка авторизации')


def get_html():
    '''Отримати html сторінку і проскролити'''
    driver.get(url)
    for i in range(how_many_pages_to_find // 10 + 1):
        sleep(1 + random.random())
        driver.execute_script('window.scrollTo(0, document.body.scrollHeight)')
        sleep(0.3 + random.random() / 3)
        if random.random() > 0.9:
            sleep(2)
    # driver.execute_script('return document.body.scrollHeight')
    # sleep(random.random())
    html = driver.page_source
    if write_on_file:
        f = open('./html', 'w', encoding='utf-8')
        f.write(html)
        f.close()
    return BeautifulSoup(html, 'html.parser')


def processing_html(soup):
    '''Оюробка html'''
    # print(soup.prettify())
    list_blok = soup.findAll('div',
                             class_='rq0escxv l9j0dhe7 du4w35lb hybvsw6c io0zqebd m5lcvass fbipl8qg nwvqtn77 k4urcfbm ni8dbmo4 stjgntxs sbcfpzgs')
    print("Знайдено = ", len(list_blok))
    # Знайдені сторінки
    list_page = []
    for i in list_blok:
        try:
            # сире посилання
            href = re.search(r'href="https://www.facebook.com.+?"', str(i)).group()[14:-1:]
            # print(str(i))
            like = re.search(r'Нравится: [0-9,]+[ тыс.]*', str(i)).group()[10::]
            if like.find('тыс') == -1:
                if int(like) < how_max_like:
                    list_page.append({
                        'name': re.search(r'a aria-label=".+?"', str(i)).group()[14:-1:].replace('&amp;', '&'),
                        'href': re.search(r'www.facebook.com.+?/', href).group(),
                        'like': int(like)
                    })
        except:
            pass

    if list_page != []:
        list_page.sort(key=lambda k: k['like'])
    print(list_page)
    f = open(name_file, 'a', encoding='utf-8')
    f.write(str(list_page))
    f.close()
    return list_page

browser_settings()  # запуск
auth_fb()  # авторизація
# go_to_page(list_page)
processing_html(get_html())  # парсінг
