'''
Сделайте 100 get запрос к ссылке (endpoint) - https://api.kanye.rest/
Создайте словарь в питоне - пример: {'No':1, 'Joke': 'some kayne joke'},
не забиваем, что к каждой шутке прилагается номер!!)
И сохраните в json формате, который прикрепите к pull request (вместе с кодом).
'''

import requests
import time
import json

jokes = []

for i in range(1,5):
    req = requests.get('https://api.kanye.rest/')
    dict = {
        'No':i,
        'Joke':req.json()['quote']
    }
    jokes.append(dict)
    print(dict)
    #time.sleep(1)

#print(jokes)
with open("hw#1_case3.json", "w") as write_f:
    json.dump(jokes, write_f)
