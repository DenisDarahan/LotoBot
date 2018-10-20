from telebot import types



# ==============================================================
# User Interface

def start_menu():
    markup = types.ReplyKeyboardMarkup()
    markup.row(types.KeyboardButton('🏡 Личный кабинет'))
    markup.row(types.KeyboardButton('🎲 Розыгрыши'))
    markup.row(types.KeyboardButton('📞 Контакты'))

    return markup



# ==============================================================
# Admin Interface

def start_admin_menu():
    markup = types.ReplyKeyboardMarkup()
    markup.row(types.KeyboardButton('🎲 Розыгрыш'))
    markup.row(types.KeyboardButton('📊 Статистика'))
    markup.row(types.KeyboardButton('↩️ Вернуться в главное меню'))

    return markup

