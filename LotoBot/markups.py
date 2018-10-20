from telebot import types

from utils import create_payment_link



# ==============================================================
# User Interface

def start_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row(types.KeyboardButton('🏡 Личный кабинет'))
    markup.row(types.KeyboardButton('🎲 Розыгрыши'))
    markup.row(types.KeyboardButton('📞 Контакты'))

    return markup


def private_room_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row(types.KeyboardButton('📥 Пополнить счет'))
    markup.row(types.KeyboardButton('📤 Вывод средств'))
    markup.row(types.KeyboardButton('↩️ Назад'))

    return markup


def raise_money_account(user_id, rubles, kopeck):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton('💸 Пополнить!', url=create_payment_link(user_id, rubles, kopeck)))

    return markup


def check_raise_money_account(msg_id):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton('🔄 Обновить информацию', callback_data='check_money_' + str(msg_id)))

    return markup



# ==============================================================
# Admin Interface

def start_admin_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row(types.KeyboardButton('🎲 Розыгрыш'))
    markup.row(types.KeyboardButton('📊 Статистика'))
    markup.row(types.KeyboardButton('↩️ Вернуться в главное меню'))

    return markup

