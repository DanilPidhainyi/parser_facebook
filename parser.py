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
url = 'https://www.facebook.com/search/pages?q=restaurant&filters=eyJmaWx0ZXJfcGFnZXNfbG9jYXRpb246MCI6IntcIm5hbWVcIjpcImZpbHRlcl9wYWdlc19sb2NhdGlvblwiLFwiYXJnc1wiOlwiMTAyMTQ2NjYzMTYwODMxXCJ9In0%3D'
# акунт фейсбук
login_facebook = ''
pass_facebook = ''
# скільки сторінок потрібно знайти
how_many_pages_to_find = 40
write_on_file = 0  # для записів сторінок у файл 1

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
        id_enter = re.search('u_0_d_..' , driver.page_source).group()
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
        sleep(random.random())
        driver.execute_script('window.scrollTo(0, document.body.scrollHeight)')
        sleep(random.random())
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
    list_blok = soup.findAll('div', class_='rq0escxv l9j0dhe7 du4w35lb hybvsw6c io0zqebd m5lcvass fbipl8qg nwvqtn77 k4urcfbm ni8dbmo4 stjgntxs sbcfpzgs')
    print("Знайдено = ", len(list_blok))
    # Знайдені сторінки
    list_page = []
    try:
        for i in list_blok:
            try:
                # сире посилання
                href = re.search(r'href="https://www.facebook.com.+?"', str(i)).group()[14:-1:]
                list_page.append({
                    'name' : re.search(r'a aria-label=".+?"', str(i)).group()[14:-1:].replace('&amp;', '&'),
                    'href' : re.search(r'www.facebook.com.+?/', href).group(),
                    'like' : re.search(r'Нравится: [0-9,]+ ', str(i)).group()[10::]
                })
                print(list(map(lambda i: i['like'], list_page)))
            except:
                print('')
    except AttributeError:
        print('щось трапилось з сторінкою')
    print(list_page)
    return list_page

def get_all_information(soup, person):
    '''отримання інформації з сторінки'''
    try:
        email = str(soup.findAll('a', class_='oajrlxb2 g5ia77u1 qu0x051f esr5mh6w e9989ue4 r7d6kgcz rq0escxv nhd2j8a9 nc684nl6 p7hjln8o kvgmc6g5 cxmmr5t8 oygrvhab hcukyx3x jb3vyjys rz4wbd8a qt6c0cv9 a8nywdso i1ao9s8h esuyzwwr f1sip0of lzcic4wl py34i1dx gpro0wi8'))\
            .replace('\n', '')

        person['email'] = re.search(r'">[a-z]+?@[a-z]+?\.[a-z]+?.*?<', email).group()[2:-1:]
    except AttributeError:
        # print(email)
        person['email'] = 'не найдено'
    print('email=', person['email'])

    try:
        phone = str(soup.findAll('span', class_='d2edcug0 hpfvmrgz qv66sw1b c1et5uql lr9zc1uh jq4qci2q a3bd9o3v knj5qynh oo9gr5id'))\
            .replace('\n', '')
        person['phone'] = re.search(r'">[+ 0-9]+?<', phone).group()[2:-1:]
    except AttributeError:
        # print(phone)
        person['phone'] = 'не найдено'
    print('phone= ', person['phone'])

    try:
        location = str(soup.findAll('span', class_='a8c37x1j ni8dbmo4 stjgntxs l9j0dhe7')).replace('\n', '')
        person['location'] = re.search(r'">[A-Za-z ,./ А-Яа-я 0-9]+?</span>', location).group()[2:-7:]
    except AttributeError:
        # print(location)
        person['location'] =  'не найдено'
    print('location= ', person['location'])
    return person

def get_date_logotype(soup, link, person):
    '''открить логотіп'''
    def get_main_photo():
        try:
            # класичний випадок
            html = str(soup.findAll('div', class_='aovydwv3 j83agx80 wkznzc2l dlu2gh78'))
            logo = re.search(link + 'photos/.*?/.*?"', html).group()[:-1:]
            logo = re.search(link + 'photos/.*/', logo).group()
            driver.get(logo)
        except AttributeError:
            try:
                # випадок коли проблеми з назвою фото
                html = str(soup.findAll('div', class_='aovydwv3 j83agx80 wkznzc2l dlu2gh78'))
                logo = re.search(r'https://www.facebook.com/.+?/photos/.*?/.*?"', html).group()[:-1:]
                logo = re.search(r'https://www.facebook.com/.+/photos/.*/', logo).group()
                driver.get(logo)
            except:
                try:
                    # випадок коли у профіля є історія і потрібно вибрати аватарку
                    driver.find_element_by_xpath("//div[@aria-label='Фото профиля Страницы']").click()
                    sleep(random.random())
                    driver.find_elements_by_xpath('//a[@role="menuitem"]')[-1].click()
                except:
                    print('logo= проблема')

    get_main_photo()
    # прогортування фото
    def turn_the_page(f=0):
        '''перевірка по силках фото'''
        try:
            old_url = ''
            while old_url != driver.current_url:
                old_url = driver.current_url
                for i in range(5):
                    driver.find_element_by_css_selector('body').send_keys(Keys.RIGHT)
                    sleep(0.1)

        except:
            if f:
                turn_the_page(1)

    turn_the_page(0)
    try:
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        html = str(soup.findAll('div', class_='dati1w0a f10w8fjw hv4rvrfc discj3wi'))
        person['data_the_first_photo'] = re.search(r'[0-9]{1,2} [A-Za-zА-Яа-я]*? [0-9]{4} г\.', html).group()
        print('data_the_first_photo=', person['data_the_first_photo'])
    except:
        person['data_the_first_photo'] = 'не найдено'


def go_to_page(list_page):
    '''Перехід на сторіну та отримання html'''
    for i in list_page:
        print(str(i['href']))
        driver.get('https://' + i['href'])
        sleep(1 + random.random())
        html = driver.page_source
        # print(html)
        if write_on_file:
            f = open('./page_html.txt', 'a', encoding='utf-8')
            f.write(str(html))
            f.close()
        print('name= ', str(i['name']))
        person = get_all_information(BeautifulSoup(html, 'html.parser'), i)
        # if (person['location'] == 'не найдено' and
        #     person['phone'] == 'не найдено' and
        #     person['email'] == 'не найдено'):
        #     print('')
        sleep(0.5)
        get_date_logotype(BeautifulSoup(html, 'html.parser'), 'https://' + i['href'], person)
        print('\n')




# processing_html(get_html(auth_fb(browser_settings())))

# запус по скачаній сторінці
# f = open('./page_html.txt', 'r', encoding='utf-8')
# html = f.read()
# f.close()

# get_all_information(BeautifulSoup(html, 'html.parser'))


# list_page = [{'name': 'Wooden Horse Restaurant & Bar', 'href': 'www.facebook.com/woodenhorserestaurant/'}, {'name': 'Jellyfish Restaurant', 'href': 'www.facebook.com/jellyfishrestaurant/'}, {'name': 'Brisbane House Hotel', 'href': 'www.facebook.com/brisbanehousehotel/'}, {'name': 'The American Diner Co.', 'href': 'www.facebook.com/americandinerco/'}, {'name': 'Birds Nest Restaurant', 'href': 'www.facebook.com/BirdsNestRest/'}, {'name': 'The Coast Bar & Restaurant, Gosford Waterfront', 'href': 'www.facebook.com/thecoastbarandrestaurantgosford/'}, {'name': 'Mado Restaurant & Cafe Brisbane', 'href': 'www.facebook.com/madorestaurant/'}, {'name': "Jo-Jo's Restaurant", 'href': 'www.facebook.com/jojosrestaurant/'}, {'name': 'Lamberts Restaurant and Bar', 'href': 'www.facebook.com/lambertsrestaurant/'}, {'name': 'Three Blue Ducks', 'href': 'www.facebook.com/ThreeBlueDucks/'}]

# processing_html(BeautifulSoup(html, 'html.parser'))

browser_settings() # запуск
auth_fb()  # авторизація
# go_to_page(list_page)
go_to_page(processing_html(get_html())) # парсінг
