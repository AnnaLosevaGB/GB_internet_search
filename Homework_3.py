# 1. Развернуть у себя на компьютере/виртуальной машине/хостинге MongoDB и реализовать функцию, которая будет добавлять
# только новые вакансии в вашу базу.
# 2. Написать функцию, которая производит поиск и выводит на экран вакансии с заработной платой больше введённой суммы
# (необходимо анализировать оба поля зарплаты). Для тех, кто выполнил задание с Росконтролем - напишите запрос для
# поиска продуктов с рейтингом не ниже введенного или качеством не ниже введенного (то есть цифра вводится одна, а
# запрос проверяет оба поля)

from pymongo import MongoClient
# from pymongo.errors import DuplicateKeyError
import json
from pprint import pprint


def try_to_add(doc):
    """Попытка добавления вакансии. Если дублируется - проверяет та ли это вакансия или ее обновили.
    Возвращает 1 в добавленную, дублирующуюся или обновленную сторону для подсчета количества."""

    result = vacancies.find_one({'_id': doc['_id']})

    if not result:
        vacancies.insert_one(doc)
        return [1, 0, 0]
    elif result['name'] == doc['name'] and result['salary_min'] == doc['salary_min'] and \
            result['salary_max'] == doc['salary_max']:
        return [0, 1, 0]
    else:
        vacancies.update_one({'_id': doc['_id']}, {"$set": {'name': doc['name'],
                                                            'salary_min': doc['salary_min'],
                                                            'salary_max': doc['salary_max']}})
        return [0, 0, 1]


def add_new(data_list):
    """Добавление новых вакансий в базу.
    Дополнительно выводит сообщение в результат - количество добавленных и количество дублирующихся вакансий."""

    count_add = 0
    count_duplicate = 0
    count_update = 0

    for data in data_list:
        # создание id
        data_id = ''
        for char in data['vacancy_link']:
            if char.isdigit():
                data_id += char

        doc = {"_id": data_id,
               "vacancy_link": data['vacancy_link'],
               "name": data['name'],
               "salary_min": data['salary_min'],
               "salary_max": data['salary_max'],
               "salary_currency": data['salary_currency'],
               "company_name": data['company'],
               "company_link": data['company_link'],
               "city": data['city'],
               "experience": data['experience'],
               "site": data['site']
               }

        result = try_to_add(doc)
        count_add += result[0]
        count_duplicate += result[1]
        count_update += result[2]

    message = f'Добалено {count_add} шт. новых вакансий, не добавлено {count_duplicate} шт., ' \
              f'обновлено {count_update} шт.'
    return message


def salary_more(min_user_salary):
    """Поиск вакансий на соответствие минимальным требованиям зарплаты.
    Возвращает список подходящих вакансий."""

    result = []
    for doc in vacancies.find({'$or': [{'salary_max': {'$gte': min_user_salary}},
                                       {'salary_max': None}
                                       ]}):
        result.append(doc)
    return result


# Задание 1

client = MongoClient('127.0.0.1', 27017)

db = client['users1506_second']

vacancies = db.vacancies

# Список данных на добавление берем из json-файла, в который сохранялись данные в ДЗ2
with open('Homework_2_output.json', 'r') as r_file:
    new_data = json.load(r_file)

print(add_new(new_data))

# Для проверки подсчет количества или вывод
# count = 0
# for doc in vacancies.find({}):
#     count += 1
# print(count)

# for doc in vacancies.find({}):
#     pprint(doc)


# Задание 2:

salary = int(input('Введите минимальную зарплату: '))
result_s = salary_more(salary)

print(f'Найдено результатов: {len(result_s)}')
for i in result_s:
    print(i['name'], i['company_name'], i['salary_min'], i['salary_max'])


