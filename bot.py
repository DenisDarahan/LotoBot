from LotoBot.config import TOKEN, admin_id
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

@bot.message_handler(commands=['admin'], func=lambda message: message.chat.id == admin_id)
def start_message(message):
    set_variables_stage(admin_id, 'admin')
    bot.send_message(message.chat.id,
                     '🏛 Добро пожаловать в админ-панель',
                     reply_markup=start_admin_menu())






if __name__ == '__main__':
    bot.polling(none_stop=True, timeout=20)
