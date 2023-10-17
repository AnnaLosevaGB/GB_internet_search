# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from pymongo import MongoClient


class JobparserPipeline:
    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.mongo_base = client.vacancies2806

    def process_item(self, item, spider):
        if spider.name == 'hhru':
            item['salary'] = self.process_salary_hh(item['salary'])
        else:
            item['salary'] = self.process_salary_sj(item['salary'])
        collection = self.mongo_base[spider.name]
        collection.insert_one(item)
        return item

    def process_salary_hh(self, salary):
        salary_min = None
        salary_max = None
        salary_currency = None
        salary_type = None
        if salary:
            if len(salary) == 6:
                if salary[0] == 'от':
                    salary_min = int(salary[1].replace('\xa0', ''))
                    salary_currency = salary[-3]
                    salary_type = salary[-1]
                elif salary[0] == 'до':
                    salary_max = int(salary[1].replace('\xa0', ''))
                    salary_currency = salary[-3]
                    salary_type = salary[-1]
            elif len(salary) == 8:
                salary_min = int(salary[1].replace('\xa0', ''))
                salary_max = int(salary[3].replace('\xa0', ''))
                salary_currency = salary[-3]
                salary_type = salary[-1]
            else:
                print(f'Check salary')
        salary_return = {
            'salary_min': salary_min,
            'salary_max': salary_max,
            'salary_currency': salary_currency,
            'salary_type': salary_type
        }
        return salary_return

    def process_salary_sj(self, salary):
        salary_min = None
        salary_max = None
        salary_currency = None
        if salary:
            if len(salary) == 4:
                if salary[2].find('\xa0₽'):
                    salary[2] = salary[2].replace('\xa0₽', '')
                    salary[2] = int(salary[2].replace('\xa0', ''))
                    salary_currency = '₽'
                if salary[0] == 'от':
                    salary_min = salary[2]
                elif salary[0] == 'до':
                    salary_max = salary[2]
            elif len(salary) == 8:
                salary_min = int(salary[0].replace('\xa0', ''))
                salary_max = int(salary[4].replace('\xa0', ''))
                salary_currency = salary[-2]
            else:
                print(f'Check salary')
        salary_return = {
            'salary_min': salary_min,
            'salary_max': salary_max,
            'salary_currency': salary_currency,
            'salary_type': None
        }
        return salary_return
