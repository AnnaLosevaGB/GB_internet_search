# Задание 2. Изучить список открытых API (https://www.programmableweb.com/category/all/apis). Найти среди них любое,
# требующее авторизацию (любого типа). Выполнить запросы к нему, пройдя авторизацию. Ответ сервера записать в файл.
# Если нет желания заморачиваться с поиском, возьмите API вконтакте (https://vk.com/dev/first_guide). Сделайте запрос,
# чтобы получить список всех сообществ на которые вы подписаны.

import requests

url = f'https://oauth.vk.com/authorize'

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 '
                  'Safari/537.36',
    'Accept': 'application/json'
}
params = {
    'client_id': '51667330',
    'redirect_uri': 'https://api.vk.com/method/groups.get',
    # 'user_id': '3195889'
}

response = requests.get(url, headers=headers, params=params)
j_data = response.json()

print(j_data, sep='\n')
