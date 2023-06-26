from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError

import time

driver = webdriver.Chrome(executable_path='chromedriver.exe')

driver.get('https://account.mail.ru/login')

elem = driver.find_element(By.NAME, 'username')
elem.send_keys('study.ai_172@mail.ru')

elem.send_keys(Keys.ENTER)

# очень медленно грузится
time.sleep(15)

elem = driver.find_element(By.NAME, 'password')
elem.send_keys('Ferrum123!')

elem.send_keys(Keys.ENTER)

# Тут требует второй раз пароль. Нажать на кнопку "Это я"
time.sleep(15)

try:
    elem = driver.find_element(By.NAME, 'password')
    elem.send_keys('Ferrum123!')
except:
    pass

# Тут проверку нужно закрыть
time.sleep(30)

profile_link = driver.find_element(By.CLASS_NAME, "js-letter-list-item").get_attribute('href')
driver.get(profile_link)


client = MongoClient('127.0.0.1', 27017)

db = client['users2606']

letters = db.letters

time.sleep(45)

while True:

    doc = {"thread": driver.find_element(By.CLASS_NAME, "thread-subject").text,
           "author": driver.find_element(By.CLASS_NAME, "letter-contact").text,
           "date": driver.find_element(By.CLASS_NAME, "letter__date").text,
           "text": driver.find_element(By.XPATH, '//tbody').text
           }

    try:
        letters.insert_one(doc)
    except DuplicateKeyError:
        pass

    try:
        edit_profile = driver.find_element(By.CLASS_NAME, "ico_16-arrow-down")
        edit_profile.click()
    except:
        break

    time.sleep(30)

# Проверка на количество добавленных писем
count = 0
for doc in letters.find({}):
    count += 1
print(count)

print()
