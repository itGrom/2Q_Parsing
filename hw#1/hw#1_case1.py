import requests

service = 'https://api.github.com/users/itGrom/repos'
headers = {'Accept: application/vnd.github.v3+json'}

req = requests.get(service)

print(f'Заголовки {req.headers}\n')
print(f'Ответ {req.text}')

for key in req.json():
    print(key['name'])
