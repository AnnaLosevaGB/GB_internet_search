# Задание 2. Изучить список открытых API (https://www.programmableweb.com/category/all/apis). Найти среди них любое,
# требующее авторизацию (любого типа). Выполнить запросы к нему, пройдя авторизацию. Ответ сервера записать в файл.
# Если нет желания заморачиваться с поиском, возьмите API вконтакте (https://vk.com/dev/first_guide). Сделайте запрос,
# чтобы получить список всех сообществ на которые вы подписаны.

import requests

# Закоменченная часть - запрос на получение токена

# url = 'https://oauth.vk.com/authorize'
#
# headers = {
#     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 '
#                   'Safari/537.36',
#     'Accept': 'application/json'
# }
# params = {
#     'client_id': '51667330',
#     'scope': 'groups',
#     'redirect_uri': 'https://oauth.vk.com/blank.html',
#     'response_type': 'token'
# }
#
# response = requests.get(url, params=params)
# # j_data = response.text()
#
# print(response.url)

token = 'vk1.a.J6va60pr0PHhQ6uZdRfrIFSlF3odbKDipYxDJeKl-8fw714v-Ly8Ho-41lgAPd3f8D1Z1E_KN2gran-ZMjvGIrGMSEJ34lCHVvsyA1ft' \
        'soKYFzQUHnJLe-NuVhp2H-fCyk8luo1GZAql7FKHA09jGs3BcYVxoHEFCuDRGdK6mFpgNEtgw7jonRwDzOuvCAUiBAcJ2yNmFiBoPhE68O0grA'

url = 'https://api.vk.com/method/groups.get'

headers = {
    # 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 '
    #               'Safari/537.36',
    'Accept': 'application/json',
    'Authorization': f'Bearer {token}'
}
params = {
    'user_id': '3195889',
    'v': '5.131',
    'extended': '1'
}

response = requests.get(url, params=params, headers=headers)

print(response.json())
