import requests
import json

dict = {}
i = 1

service = 'https://api.github.com/users/itGrom/repos'
headers = {'Accept: application/vnd.github.v3+json'}

req = requests.get(service)

#print(f'Заголовки {req.headers}\n')
#print(f'Ответ {req.text}')

for key in req.json():
#    print(f"'Repository{i}':'{key['name']}'")
    dict[f"Repository{i}"] = key['name']
    i+=1

with open ('my_repo.json', 'w') as write_f:
    json.dump(dict, write_f)
