import requests
from bs4 import BeautifulSoup as bs
import pandas as pd
import json
import lxml
import re

headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36'}

vacancy = 'инженер'
page = 2

result_list = []
dict_result = {}

for i in range(page):

    links = {'https://hh.ru': {'params': {'text': vacancy,
                                          'page': i},
                               'search': '/search/vacancy'},
             'https://russia.superjob.ru': {'params': {'keywords': vacancy,
                                                       'page': i},
                                            'search': '/vacancy/search'}}

    for link, value in links.items():
        vacancy_a_tag = ''
        vacancy_link = ''
        vacancy_name = ''
        salary_min = ''
        salary_max = ''
        salary_period = ''

        req = requests.get(link + value['search'], headers=headers, params=value['params'])

        soup = bs(req.content, 'lxml')

        if (link == 'https://hh.ru'):
            div_tag_all = soup.find_all(attrs = {'class' : re.compile('^.*vacancy-serp-item__row_header$')})


            for div_tag in div_tag_all:
                vacancy_name = ''
                salary_min = ''
                salary_max = ''
                salary_period = ''


                vacancy_link = div_tag.find_next('a')['href']

                vacancy_name = div_tag.find_next('a').string

                salary_span_tag = [el for el in div_tag.find_next(attrs = {'class' : 'vacancy-serp-item__sidebar'}).stripped_strings]

                if (len(salary_span_tag) == 1):
                    salary_min = salary_span_tag[0].split(' ')[0]
                    salary_max = salary_span_tag[0].split(' ')[2]

                if (len(salary_span_tag) > 1):
                    salary_min = salary_span_tag[0]
                    salary_max = salary_span_tag[1]

                result_list.append([vacancy_name, salary_min, salary_max, salary_period, vacancy_link, link])

        if (link == 'https://russia.superjob.ru'):
            div_tag_all = soup.find_all(attrs = {'class' : re.compile('^.*f-test-vacancy-item.*$')})


            for div_tag in div_tag_all:
                vacancy_name = ''
                salary_min = ''
                salary_max = ''
                salary_period = ''

                vacancy_a_tag = div_tag.find_next(attrs = {'class' : re.compile('^.*f-test-link.*$')}).contents
                vacancy_link = link + div_tag.find_next(attrs = {'class' : re.compile('^.*f-test-link.*$')})['href']

                for i in vacancy_a_tag:
                    vacancy_name += i.string

                salary_span_tag = div_tag.find_next(attrs = {'class' : re.compile('^.*f-test-text-company-item-salary.*$')}).contents

                if (len(salary_span_tag) == 1):
                    salary_min = salary_span_tag[0].string
                else:
                    salary_span_child = div_tag.find_next(attrs = {'class' : re.compile('^.*f-test-text-company-item-salary.*$')}).next.next.contents

                    salary_min = salary_span_child[0].string

                    if (salary_span_child[1].name == 'span'):
                        salary_max = salary_span_child[2].string
                    if (salary_span_child[1].name != 'span'):
                        salary_max = salary_span_child[4].string

                    salary_period = div_tag.find_next(attrs = {'class' : re.compile('^.*f-test-text-company-item-salary.*$')}).next.next_sibling.contents[1].string


                result_list.append([vacancy_name, salary_min, salary_max, salary_period, vacancy_link, link])
                
res_df = pd.DataFrame(result_list, columns=['vacancy_name', 'salary_min', 'salary_max', 'salary_period', 'vacancy_link', 'link'])
print(res_df)