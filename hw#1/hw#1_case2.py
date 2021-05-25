import requests
import json

headers = {'Authorization': 'Bearer ilhKfbi6Rq3pYK67IHBO'}

req = requests.get('https://the-one-api.dev/v2/character', headers=headers)

data = req.json()

with open("hw#1_case2.json", "w") as write_f:
    json.dump(data, write_f)

print(data)