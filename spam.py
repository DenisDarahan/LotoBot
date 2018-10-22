from celery import Celery
import telebot
import time
from telebot.apihelper import ApiException
from LotoBot.config import TOKEN

app = Celery('tasks', broker='redis://localhost')
bot = telebot.TeleBot(TOKEN)


@app.task
def send_spam(text, users):
    for user in users:
        try:
            bot.send_message(user[0],
                             text,
                             parse_mode='HTML')
            time.sleep(0.05)
        except ApiException:
            continue
