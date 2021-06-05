import requests
from bs4 import BeautifulSoup as bs
import pandas as pd
import json
import lxml
import re
from pymongo import MongoClient
from pprint import pprint

headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36'}

vacancy = 'инженер'
page = 2

result_list = []
result_dict = {}

for i in range(page):

    links = {'https://hh.ru': {'params': {'text': vacancy,
                                          'page': i},
                               'search': '/search/vacancy'},
             'https://russia.superjob.ru': {'params': {'keywords': vacancy,
                                                       'page': i + 1},
                                            'search': '/vacancy/search'}}

    for link, value in links.items():
        vacancy_a_tag = None
        vacancy_link = None
        vacancy_name = ''
        salary_min = float('NaN')
        salary_max = float('NaN')
        salary_currency = None
        salary_period = None



        req = requests.get(link + value['search'], headers=headers, params=value['params'])

        soup = bs(req.content, 'lxml')

        if (link == 'https://hh.ru'):
            div_tag_all = soup.find_all(attrs = {'class' : re.compile('^.*vacancy-serp-item__row_header$')})


            for div_tag in div_tag_all:
                vacancy_name = ''
                salary_min = float('NaN')
                salary_max = float('NaN')
                salary_currency = None
                salary_period = None
                result_dict = {}


                vacancy_link = div_tag.find_next('a')['href']

                vacancy_name = div_tag.find_next('a').string

                salary_span_tag = [el for el in div_tag.find_next(attrs = {'class' : 'vacancy-serp-item__sidebar'}).stripped_strings]

                if (len(salary_span_tag) == 1):
                    if (len(salary_span_tag[0].split(' '))) == 4:
                        salary_min = int(salary_span_tag[0].split(' ')[0].replace('\u202f', ''))
                        salary_max = int(salary_span_tag[0].split(' ')[2].replace('\u202f', ''))
                        salary_currency = salary_span_tag[0].split(' ')[3]
                    elif (len(salary_span_tag[0].split(' '))) == 3:
                        salary_currency = salary_span_tag[0].split(' ')[2]
                        if (salary_span_tag[0].split(' ')[0] == 'от'):
                            salary_min = salary_span_tag[0].split(' ')[1].replace('\u202f', '')
                            salary_max = float('NaN')
                        elif (salary_span_tag[0].split(' ')[0] == 'до'):
                            salary_max = salary_span_tag[0].split(' ')[1].replace('\u202f', '')
                            salary_min = float('NaN')


                result_dict['vacancy_category'] = vacancy
                result_dict['vacancy_name'] = vacancy_name
                result_dict['salary_min'] = salary_min
                result_dict['salary_max'] = salary_max
                result_dict['salary_currency'] = salary_currency
                result_dict['salary_period'] = salary_period
                result_dict['vacancy_link'] = vacancy_link
                result_dict['link'] = link

                result_list.append(result_dict)
                # result_list.append([vacancy_name, salary_min, salary_max, salary_period, vacancy_link, link])

        if (link == 'https://russia.superjob.ru'):
            div_tag_all = soup.find_all(attrs = {'class' : re.compile('^.*f-test-vacancy-item.*$')})


            for div_tag in div_tag_all:
                vacancy_name = ''
                salary_min = float('NaN')
                salary_max = float('NaN')
                salary_currency = None
                salary_period = None
                result_dict = {}

                vacancy_a_tag = div_tag.find_next(attrs = {'class' : re.compile('^.*f-test-link.*$')}).contents
                vacancy_link = link + div_tag.find_next(attrs = {'class' : re.compile('^.*f-test-link.*$')})['href']

                for i in vacancy_a_tag:
                    vacancy_name += i.string.replace('\n', '')

                salary_span_tag = div_tag.find_next(attrs = {'class' : re.compile('^.*f-test-text-company-item-salary.*$')}).contents

                if (len(salary_span_tag) == 1):
                    # salary_min = salary_span_tag[0].string
                    salary_min = float('NaN')
                    salary_max = float('NaN')
                else:
                    salary_span_child = div_tag.find_next(attrs = {'class' : re.compile('^.*f-test-text-company-item-salary.*$')}).next.next.contents

                    if (len(salary_span_child) == 7):
                        salary_min = int(salary_span_child[0].replace('\xa0', ''))
                        salary_max = int(salary_span_child[2].replace('\xa0', ''))
                        salary_currency = salary_span_child[6].replace('\xa0', '')
                    elif (len(salary_span_child) == 5):
                        if (salary_span_child[0] == 'от'):
                            salary_min = int(salary_span_child[4].split('\xa0')[0] + salary_span_child[4].split('\xa0')[1])
                            salary_max = float('NaN')
                            salary_currency = salary_span_child[4].split('\xa0')[2]
                        elif (salary_span_child[0] == 'до'):
                            salary_max = int(salary_span_child[4].split('\xa0')[0] + salary_span_child[4].split('\xa0')[1])
                            salary_min = float('NaN')
                            salary_currency = salary_span_child[4].split('\xa0')[2]
                        else:
                            salary_max = int(salary_span_child[0].replace('\xa0', ''))
                            salary_min = int(salary_span_child[0].replace('\xa0', ''))
                            salary_currency = salary_span_child[4]



                    salary_period = div_tag.find_next(attrs = {'class' : re.compile('^.*f-test-text-company-item-salary.*$')}).next.next_sibling.contents[1].string

                result_dict['vacancy_name'] = vacancy_name
                result_dict['salary_min'] = salary_min
                result_dict['salary_max'] = salary_max
                result_dict['salary_currency'] = salary_currency
                result_dict['salary_period'] = salary_period
                result_dict['vacancy_link'] = vacancy_link
                result_dict['link'] = link


                result_list.append(result_dict)


def insert_db(data):
    client = MongoClient('localhost', 27017)
    db = client['test_db']
    job_parsing = db.job_parsing
    list_with_id = []

    for el in data:
        new_el = el.copy()
        new_el['_id'] = el['vacancy_link'].split('?')[0]
        list_with_id.append(new_el)

    # job_parsing.delete_many({})
    try:
        job_parsing.insert_many(list_with_id)
    except Exception as err:
        print(err)

insert_db(result_list)


def select_db(salary):
    client = MongoClient('localhost', 27017)
    db = client['test_db']
    job_parsing = db.job_parsing

    return job_parsing.find( { '$or': [ { 'salary_min' : { '$gt' : salary } }, { 'salary_max' : { '$gt' : salary } } ] } )


list = select_db(85000)

for doc in list:
    pprint(doc)