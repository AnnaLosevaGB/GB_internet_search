# Задание. Необходимо собрать информацию о вакансиях на вводимую должность (используем input или через аргументы
# получаем должность) с сайта HH. Приложение должно анализировать все страницы сайта. Получившийся список должен
# содержать в себе минимум:
# Наименование вакансии.
# Предлагаемую зарплату (разносим в три поля: минимальная и максимальная и валюта. цифры преобразуем к цифрам).
# Ссылку на саму вакансию.
# Сайт, откуда собрана вакансия.
# По желанию можно добавить ещё параметры вакансии (например, работодателя и расположение). Общий результат можно
# вывести с помощью dataFrame через pandas. Сохраните в json либо csv.

import requests
from bs4 import BeautifulSoup
import json

# post = input('Введите должность: ')
post = 'sadovnik'

base_url = 'https://hh.ru'

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 '
                  'Safari/537.36'
}

params = {'page': 0}

url = f'{base_url}/vacancies/{post}'

session = requests.Session()

vacancies_list = []

while True:

    response = session.get(url, headers=headers, params=params)

    dom = BeautifulSoup(response.text, 'html.parser')

    vacancies = dom.find_all('div', {'class': 'serp-item'})

    for vacancy in vacancies:
        vacancy_data = {}

        info = vacancy.find('a', {'class': 'serp-item__title'})
        link = info['href']
        name = info.getText()

        company = vacancy.find('div', {'class': 'vacancy-serp-item__meta-info-company'})
        company_name = company.getText()
        try:
            company_link = base_url + company.next.attrs['href']
        except AttributeError:
            company_link = None

        city = vacancy.find('div', {'data-qa': 'vacancy-serp__vacancy-address'}).getText()
        experience = vacancy.find('div', {'data-qa': 'vacancy-serp__vacancy-work-experience'}).getText()

        salary = vacancy.find('span', {'data-qa': 'vacancy-serp__vacancy-compensation'})

        salary_max = None
        salary_min = None
        salary_currency = None

        if salary:
            salary = salary.text
            salary_list = salary3 = salary.replace('\u202f', '').split()
            salary_currency = salary_list[-1]
            if salary_list[0] == 'от':
                salary_min = int(salary_list[1])
            elif salary_list[0] == 'до':
                salary_max = int(salary_list[1])
            elif salary_list[1] == '–':
                salary_min = int(salary_list[0])
                salary_max = int(salary_list[2])
            else:
                print(f'Check salary in page={params["page"]} name={name} company={company}')

        vacancy_data['vacancy_link'] = link
        vacancy_data['name'] = name
        vacancy_data['salary_min'] = salary_min
        vacancy_data['salary_max'] = salary_max
        vacancy_data['salary_currency'] = salary_currency
        vacancy_data['company'] = company_name
        vacancy_data['company_link'] = company_link
        vacancy_data['city'] = city
        vacancy_data['experience'] = experience
        vacancy_data['site'] = base_url

        vacancies_list.append(vacancy_data)

    if dom.find_all('a', {'data-qa': 'pager-next'}):
        params['page'] += 1
    else:
        break

with open('Homework_2_output.json', 'w') as write_file:
    json.dump(vacancies_list, write_file)

print(len(vacancies_list))
