from LotoBot.config import TOKEN
import telebot



bot = telebot.TeleBot(TOKEN)




# ==============================================================
# User Interface

@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id,
                     '')




# ==============================================================
# Admin Interface

@bot.message_handler(commands=['admin'])
def start_message(message):
    bot.send_message(message.chat.id,
                     '')