import time
import urllib.request
import requests
from html.parser import HTMLParser
import os
import telebot
from config import *

URL = 'https://api.telegram.org/bot'  # URL на который отправляется запрос
bot = telebot.TeleBot(token)
# data = {'offset': offset + 1, 'limit': 0, 'timeout': 0}
debug = 0


@bot.message_handler(commands=['ping'])
def ping(hostname):
    response = os.system("ping -c 1 " + hostname.text[5:])
    if response == 0:
        return hostname.text[5:] + " is up"
    else:
        return hostname.text[5:] + " is down"


@bot.message_handler(commands=['w'])
def get_weather(message):
    result = ''
    w = get_page("http://www.tatarmeteo.ru/")
    index = w.find('<div class="pogoda"><h3>Текущая погода по г. Казани</h3>')
    if index != -1:
        w = w[index:len(w)]
        index = w.find('</table>')
        if index != -1:
            w = w[0:index]
            p = MyHTMLParser()
            p.feed(w)
            p.close()
            result = p.data
        return result
    else:
        return 'Weather not found!'


class MyHTMLParser(HTMLParser):
    # def __init__(self):

    def reset(self):
        HTMLParser.reset(self)
        # HTMLParser.__init__(self)
        self.data = ''

    def handle_data(self, data):
        print("Encountered some data  :", data)
        self.data += data + ' '


def get_page(url):
    r = requests.get(url)
    if r.status_code == 200:
        page = r.text
    return page


if __name__ == '__main__':
    bot.polling(none_stop=True)
