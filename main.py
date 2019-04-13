import wikipediaapi
import telebot
from telebot import types
import time

def wikipedia_api(topic):
   wiki_wiki = wikipediaapi.Wikipedia('ru')
   page_py = wiki_wiki.page(topic)

   return page_py.summary, page_py.fullurl

knownUsers = {}

TOKEN = '876141696:AAGKKjDdD6XwcH9J__zxWrx7Fefraw3x9D4'

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def command_start(m):
   cid = m.chat.id
   answer = 'Привет! Я - Wikipedia Telegram-бот. Напиши команду /discover, чтобы узнать информацию, которая тебя интересует.'
   markup = types.ReplyKeyboardMarkup()
   markup.row('/discover', '/info')
   bot.send_message(cid, answer, reply_markup=markup)
   bot.send_message(cid, answer)
   knownUsers[cid] = {}
   knownUsers[cid]['prevMessage'] = m.text

@bot.message_handler(commands=['discover'])
def command_discover(m):
   cid = m.chat.id
   answer = 'Отлично! Теперь укажи интересующую тебя тему:'
   bot.send_message(cid, answer)
   knownUsers[cid]['prevMessage'] = m.text

@bot.message_handler(func=lambda message: True, content_types=['text'])
def simple_text(m):
   cid = m.chat.id
   prevMessage = knownUsers[cid]['prevMessage']
   if prevMessage == '/discover':
      text, url = wikipedia_api(m.text)
      bot.send_message(cid, text)
      time.sleep(2)
      bot.send_message(cid, 'Больше можно прочитать по ссылке:\n' + url)
   else:
      answer = 'Извини, но я тебя не понимаю :('
      bot.send_message(cid, answer)
   knownUsers[cid]['prevMessage'] = m.text

bot.polling()