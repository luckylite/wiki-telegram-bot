import requests
from bs4 import BeautifulSoup as bs
import wikiapi
import telebot
from telebot import types
import time

def wikipedia_api(topic):
   wiki_wiki = wikiapi.Wikipedia('ru')
   page_py = wiki_wiki.page(topic)

   return page_py.summary, page_py.fullurl

def get_weather(town):
   headers = {
      'accept': '*/*',
      'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'
   }

   url = 'https://sinoptik.ua/погода-' + town

   session = requests.Session()
   request = session.get(url, headers = headers)

   if request.status_code == 200:
      soup = bs(request.content, 'html.parser')
      table = soup.find('table', attrs = {'class': 'weatherDetails'})
      tr = table.find('tr', attrs = {'class': 'img'})
      td = tr.find('td', attrs = {'class': 'cur'})
      weather = td.find('div', attrs = {'class': 'weatherIco'})['title']

      temp = soup.find('p', attrs = {'class': 'today-temp'}).text

      return temp + ', ' + weather, url

   else:
      return False

TOKEN = '876141696:AAGKKjDdD6XwcH9J__zxWrx7Fefraw3x9D4'

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def command_start(m):
   user_markup = types.ReplyKeyboardMarkup(1)
   user_markup.row('/discover','/weather')
   cid = m.chat.id
   answer = 'Привет! Я - Wikipedia Telegram-бот. Напиши команду /discover, чтобы узнать информацию, которая тебя интересует. Также с помощью команды /weather ты можешь узнать погоду в своем городе.'
   bot.send_message(cid, answer, reply_markup=user_markup)

@bot.message_handler(commands=['discover'])
def command_discover(m):
   cid = m.chat.id
   answer = 'Отлично! Теперь укажи интересующую тебя тему:'
   msg = bot.send_message(cid, answer)
   bot.register_next_step_handler(msg, enter_discover)

@bot.message_handler(commands=['weather'])
def command_weather(m):
   cid = m.chat.id
   answer = 'Отлично! Теперь укажи свой город:'
   msg = bot.send_message(cid, answer)
   bot.register_next_step_handler(msg, enter_town)

@bot.message_handler(func=lambda message: True, content_types=['text'])
def simple_text(m):
   cid = m.chat.id
   answer = 'Извини, но я тебя не понимаю :('
   bot.send_message(cid, answer)

def enter_discover(m):
   cid = m.chat.id
   text, url = wikipedia_api(m.text)
   bot.send_message(cid, text)
   time.sleep(2)
   bot.send_message(cid, 'Больше можно прочитать по ссылке:\n' + url)

def enter_town(m):
   cid = m.chat.id
   text, url = get_weather(m.text)
   bot.send_message(cid, text)
   time.sleep(2)
   bot.send_message(cid, 'Подробнее можно узнать по ссылке:\n' + url)

bot.polling()