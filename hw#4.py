import requests
from lxml import html
from pprint import pprint
from datetime import datetime, date
import hashlib

header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36'}

urls = {'lenta.ru': 'https://lenta.ru',
       'mail.ru': 'https://news.mail.ru',
       'yandex.ru': 'https://yandex.ru/news'}

today = [date.strftime(date.today(),'%d %B')]
news = []
result_dict = {}


for key, link in urls.items():
    resp = requests.get(link, headers=header)
    dom = html.fromstring(resp.text)

    if (key == 'lenta.ru'):
        items_news = dom.xpath('//div[@class = "item"]')
        items_article = dom.xpath('//div[starts-with(@class, "item ")]')

        for el in items_news:
            item_name = el.xpath('./a/text()')
            item_source = key

            if (len(el.xpath('.//time/@title')) > 0):
                item_time = el.xpath('.//time/@title')
            else:
                item_time = today

            if (''.join(el.xpath('./a/@href')).find('https://') >= 0):
                item_link = el.xpath('./a/@href')
            else:
                item_link = [link + ''.join(el.xpath('./a/@href'))]

            result_dict['item_name'] = ''.join(item_name).replace('\xa0', ' ')
            result_dict['item_link'] = ''.join(item_link).replace('\xa0', ' ')
            result_dict['item_time'] = ''.join(item_time).replace('\xa0', ' ')
            result_dict['item_source'] = ''.join(item_source).replace('\xa0', ' ')
            result_dict['_id'] = hashlib.md5(''.join(item_link).encode()).hexdigest()

            news.append(result_dict)
            result_dict = {}

        for el in items_article:

            if (len(el.xpath('.//span[contains(@class, "g-date")]/text()')) > 0 and el.xpath('.//span[contains(@class, "g-date")]/text()')[0] != 'Сегодня'):
                item_time = el.xpath('.//span[contains(@class, "g-date")]/text()')
            else:
                item_time = today

            item_name = el.xpath('(.//a[@class = "titles"]//text())[last()]') if (el.xpath('(.//a[@class = "titles"]//text())[last()]')[0].replace('\xa0', '')) else el.xpath('(.//a[@class = "titles"]//text())[last()-1]')
            item_link = el.xpath('.//a[@class = "titles"]/@href')

            if (''.join(el.xpath('.//a[@class = "titles"]/@href')).find('https://') >= 0):
                item_link = el.xpath('.//a[@class = "titles"]/@href')
            else:
                item_link = [urls[key] + ''.join(el.xpath('.//a[@class = "titles"]/@href'))]


            item_source = key

            result_dict['item_name'] = ''.join(item_name).replace('\xa0', ' ')
            result_dict['item_link'] = ''.join(item_link).replace('\xa0', ' ')
            result_dict['item_time'] = ''.join(item_time).replace('\xa0', ' ')
            result_dict['item_source'] = ''.join(item_source).replace('\xa0', ' ')
            result_dict['_id'] = hashlib.md5(''.join(item_link).encode()).hexdigest()
            news.append(result_dict)
            result_dict = {}

    elif (key == 'mail.ru'):
        items_news = dom.xpath('//div[starts-with(@class, "daynews__item")]')
        # items_article = dom.xpath('//div[starts-with(@class, "item ")]')


        for el in items_news:
            item_name = el.xpath('./a//text()')
            item_source = key
            item_link = el.xpath('./a/@href')
            item_time = today

            result_dict['item_name'] = ''.join(item_name).replace('\xa0', ' ')
            result_dict['item_link'] = ''.join(item_link).replace('\xa0', ' ')
            result_dict['item_time'] = ''.join(item_time).replace('\xa0', ' ')
            result_dict['item_source'] = ''.join(item_source).replace('\xa0', ' ')
            result_dict['_id'] = hashlib.md5(''.join(item_link).encode()).hexdigest()

            news.append(result_dict)
            result_dict = {}
    elif (key == 'yandex.ru'):
        items_news = dom.xpath('//article[starts-with(@class, "mg-card")]')

        for el in items_news:
            item_name = el.xpath('.//h2[@class = "mg-card__title"]//text()')
            item_source = key
            item_link = el.xpath('.//a[@class = "mg-card__link"]/@href')
            item_time = today

            result_dict['item_name'] = ''.join(item_name).replace('\xa0', ' ')
            result_dict['item_link'] = ''.join(item_link).replace('\xa0', ' ')
            result_dict['item_time'] = ''.join(item_time).replace('\xa0', ' ')
            result_dict['item_source'] = ''.join(item_source).replace('\xa0', ' ')
            result_dict['_id'] = hashlib.md5(''.join(item_link).encode()).hexdigest()

            news.append(result_dict)
            result_dict = {}

pprint(news)

