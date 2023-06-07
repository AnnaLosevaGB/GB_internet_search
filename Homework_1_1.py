# Задание 1. Посмотреть документацию к API GitHub, разобраться как вывести список репозиториев для конкретного
# пользователя, сохранить JSON-вывод в файле *.json.

import requests

token = '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'
user = "AnnaLosevaGB"
url = f"https://api.github.com/users/{user}/repos"
headers = {
    'Authorization': f'token {token}',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 '
                  'Safari/537.36',
    'Accept': 'application/json'
}
params = {
    'state': 'open',
}

response = requests.get(url, headers=headers, params=params)
j_data = response.json()

repo_list = []
for i in j_data:
    repo_list.append(i['name'])

print(*repo_list, sep='\n')
