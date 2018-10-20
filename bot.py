from LotoBot.config import TOKEN, admin_id
from LotoBot.markups import *
from LotoBot.db_manager import *
from utils import *

import telebot



bot = telebot.TeleBot(TOKEN)




# ==============================================================
# User Interface

@bot.message_handler(commands=['start'])
def start_user_message(message):
    create_user(message.chat.id, message.chat.first_name)
    bot.send_message(message.chat.id,
                     'Добро пожаловать в LotoBot!',
                     reply_markup=start_menu())


@bot.message_handler(func=lambda message: message.text == '📞 Контакты' and
                                          get_variables_stage(message.chat.id) == 'user')
def get_contacts_user_message(message):
    bot.send_message(message.chat.id,
                     'По всем вопросам обращайтесь к администратору бота 👨‍💻 @DenisDarahan',  # TODO: change admin
                     reply_markup=start_menu())


@bot.message_handler(func=lambda message: message.text == '🏡 Личный кабинет' and
                                          get_variables_stage(message.chat.id) == 'user')
def get_private_room_user_message(message):
    bot.send_message(message.chat.id,
                     '🏡   <b>Личный кабинет</b>   🏡\n\n'
                     '💳 Ваш текущий баланс: {} руб\n'
                     '🎲 Участий в розыгрышах: {} раз(а)'
                     ''.format(*get_variables_private_room_info(message.chat.id)),
                     parse_mode='HTML',
                     reply_markup=private_room_menu())


@bot.message_handler(func=lambda message: message.text == '↩️ Назад' and
                                          get_variables_stage(message.chat.id) == 'user')
def get_contacts_user_message(message):
    bot.send_message(message.chat.id,
                     '📰 <b>Главное меню</b>',
                     parse_mode='HTML',
                     reply_markup=start_menu())


@bot.message_handler(func=lambda message: message.text == '📥 Пополнить счет' and
                                          get_variables_stage(message.chat.id) == 'user')
def start_raise_money(message):
    msg = bot.send_message(message.chat.id,
                           'Укажите, пожалуйста, сумму пополнения:',
                           reply_markup=private_room_menu())
    bot.register_next_step_handler(msg, get_amount_to_raise)


def get_amount_to_raise(message):
    result = get_float_from_message(message.text)
    if result == 'exit':
        bot.send_message(message.chat.id,
                         '📰 <b>Главное меню</b>',
                         parse_mode='HTML',
                         reply_markup=start_menu())
    elif result == 'not a number':
        bot.send_message(message.chat.id,
                         'Кажется, Вы ввели не число...\n'
                         'Укажите, пожалуйста, сумму пополнения снова:',
                         reply_markup=private_room_menu())
    else:
        msg = bot.send_message(message.chat.id,
                               'Принято!\n'
                               'Сумма пополнения: {} руб {} коп\n'
                               'Для подтверждения оплаты нажмите кнопку под этим сообщением ⬇️\n\n'
                               '❗️❗️❗️   <b>ВАЖНО</b>   ❗️❗️❗️\n'
                               '<i>Будьте внимательны - изменять комментарий к оплате НЕЛЬЗЯ!\n'
                               'В противном случае Вы рискуете потерять Ваши деньги!</i>'.format(*result),
                               parse_mode='HTML',
                               reply_markup=raise_money_account(message.chat.id, *result))
        time.sleep(3)
        bot.send_message(message.chat.id,
                         'После отправки платежа, пожалуйста, нажмите кнопку ниже ⬇️\n'
                         'Она проверит, прошла ли оплата',
                         reply_markup=check_raise_money_account(msg.message_id))


@bot.callback_query_handler(func=lambda call: call.data[:12] == 'check_money_')
def check_raise_money_payment_message(call):
    res = check_payment(call.message.chat.id)
    if res:
        msg_id = int(call.data[12:])
        update_variables_cur_payment(call.message.chat.id, '')
        real_amount = update_variables_amount(call.message.chat.id, res)
        bot.delete_message(call.message.chat.id, msg_id)
        bot.delete_message(call.message.chat.id, msg_id + 1)
        bot.send_message(call.message.chat.id,
                         '<b>Баланс успешно пополнен!</b>\n\n'
                         '    + {:.2f} 💴 RUB\n'
                         '💳 Ваш текущий баланс: {:.2f} руб'.format(res, real_amount),
                         parse_mode='HTML',
                         reply_markup=private_room_menu())
        bot.answer_callback_query(call.id, 'Успех!')
    else:
        bot.answer_callback_query(call.id, 'Оплата еще не прошла. Попробуйте проверить позже')




# ==============================================================
# Admin Interface

@bot.message_handler(commands=['admin'], func=lambda message: message.chat.id == admin_id)
def start_admin_message(message):
    update_variables_stage(admin_id, 'admin')
    bot.send_message(message.chat.id,
                     '🏛 Добро пожаловать в админ-панель',
                     reply_markup=start_admin_menu())


@bot.message_handler(func=lambda message: message.text == '↩️ Вернуться в главное меню' and
                                          get_variables_stage(message.chat.id) == 'admin')
def get_to_main_menu_admin_message(message):
    update_variables_stage(admin_id, 'user')
    bot.send_message(message.chat.id,
                     '📰 <b>Главное меню</b>',
                     parse_mode='HTML',
                     reply_markup=start_menu())


@bot.message_handler(func=lambda message: message.text == '📊 Статистика' and
                                          get_variables_stage(message.chat.id) == 'admin')
def get_statistic_admin_message(message):
    bot.send_message(message.chat.id,
                     '📊    <b>Статистика</b>\n\n'
                     'Проведенных розыгрышей: {}\n'
                     'Сумма собранных банков: {} руб\n'
                     'Заработок: {} руб'.format(*get_statistic_all()),
                     parse_mode='HTML',
                     reply_markup=start_admin_menu())




if __name__ == '__main__':
    bot.polling(none_stop=True, timeout=20)
