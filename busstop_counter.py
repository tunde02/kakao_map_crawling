from city_names import city_names # 시군구 이름들이 저장된 파일

import requests
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
from time import sleep


url = 'https://map.kakao.com/'

options = webdriver.ChromeOptions()
# options.add_argument('headless')
options.add_experimental_option("excludeSwitches", ["enable-logging"])
driver = webdriver.Chrome(executable_path='./chromedriver.exe', options=options)
driver.implicitly_wait(3)

driver.get(url)
driver.find_element_by_css_selector('.layer_body').click()

searchBox = driver.find_element_by_id('search.keyword.query')

contents = ''
order = 0
for name in city_names:
    if order == 1:
        driver.find_element_by_css_selector('.layer_body').click()
    searchBox.clear()
    searchBox.send_keys('{} 버스정류장'.format(name))
    driver.find_element_by_id('search.keyword.submit').click()

    sleep(0.5) # 이게 있어야 값이 나온 다음 버스정류장 개수를 읽어올 수 있음
    count = driver.find_element_by_xpath('//*[@id="info.search.busstops.cnt"]').text

    contents += '{}\t{}\n'.format(name, count)
    print('{} 버스정류장 개수 : {}'.format(name, count))
    order += 1

with open('시군구별 버스정류장 개수.txt', 'w', encoding='utf-8') as f:
    f.write(contents)