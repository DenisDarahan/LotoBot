from LotoBot.config import TOKEN
from LotoBot.markups import *
from LotoBot.db_manager import *
from utils import *

import telebot



bot = telebot.TeleBot(TOKEN)




# ==============================================================
# User Interface

@bot.message_handler(commands=['start'])
def start_message(message):
    create_user(message.chat.id, message.chat.first_name)
    bot.send_message(message.chat.id,
                     'Добро пожаловать в LotoBot!',
                     reply_markup=start_menu())







# ==============================================================
# Admin Interface

@bot.message_handler(commands=['admin'])
def start_message(message):
    bot.send_message(message.chat.id,
                     'Добро пожаловать в админ-панель')



if __name__ == '__main__':
    bot.polling(none_stop=True, timeout=20)
