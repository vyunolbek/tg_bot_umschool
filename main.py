import telebot
import requests
import json
from time import sleep
from random import randint
token = "TG BOT TOKEN"
bot = telebot.TeleBot(token)

cache_id = set()

def dz(message):
    i = 0

    s = requests.Session()

    payload = {
        # "next": "/profile/",
        "csrfmiddlewaretoken": "UMSCHOOL TOKEN",
        "login": "e-mail",
        "password": "PASSOWRD"
    }

    headers = {
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "accept-language": "ru,en;q=0.9",
        "cache-control": "max-age=0",
        "content-type": "application/x-www-form-urlencoded",
        "sec-ch-ua": "\" Not A;Brand\";v=\"99\", \"Chromium\";v=\"96\", \"Yandex\";v=\"22\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Windows\"",
        "sec-fetch-dest": "document",
        "sec-fetch-mode": "navigate",
        "sec-fetch-site": "same-origin",
        "sec-fetch-user": "?1",
        "upgrade-insecure-requests": "1",
        "cookie": "csrftoken=6iEzjv3Tzt4l6xb08SRFTfnZw58xDZ8KoVbWnBBqwstRoNUmsCDBxlwVcrk3Q4cU; _ym_uid=16450833881068981921; _ym_d=1645083388; _gcl_au=1.1.64348424.1645083388; _ym_isad=2; _ym_visorc=w; _ga_GXM0VHFWY1=GS1.1.1645083388.1.0.1645083388.60; _ga=GA1.2.2036954509.1645083388; _gid=GA1.2.546071677.1645083388; _dc_gtm_UA-188282956-1=1; amp_fc3d9f=duetr1P6hGR9FeHZcppw7e...1fs39oqk6.1fs39oqk6.0.0.0; st_uid=9e0e0d95cbb60a2fc1dcb165df7a3134",
        "Referer": "https://umschool.net/accounts/login/?next=/profile/",
        "Referrer-Policy": "same-origin"
    }

    r = s.post('https://umschool.net/accounts/login/', data=payload, headers=headers)

    print(r.status_code)

    if r.status_code != 200:
        bot.send_message(message.chat.id, "Нужно менять токен")
        return -10

    payload2 = {
        "pool": "true",
        "product_type": "mg",
        "limit": "1000",
        "offset": "0"
    }

    g = s.get("https://umschool.net/api/homework/pool/", params=payload2)

    print(g.status_code)

    result = json.loads(g.text)

    result = result['results']
    not_checked = list(filter(lambda x: x['status'] == 'DONE', result))

    for item in not_checked:
        if item['id'] not in cache_id:
            to_tg = f"{item['student']}\n{item['homework']['title']}\nСтоимость: {item['price']}\nСсылка на пул: https://umschool.net/homework/pool/"
            bot.send_message(message.chat.id, to_tg)

    cache_id.clear()
    cache_id.update(list(map(lambda x: x['id'], not_checked)))


@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, "Привет! Проверяю домашки")
    while True:
        dz(message)
        sleep(10 + randint(5, 23))



bot.infinity_polling()
