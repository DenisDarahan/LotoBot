import time
import hashlib
import requests

from LotoBot.config import PAY_LINK, url_get_history_payed, headers
from LotoBot.db_manager import *



def get_number_from_message(func):
    def wrapper(text):
        try:
            result = func(text)
        except ValueError:
            if text in ['↩️ Назад', '❌ Отмена']:
                result = 'exit'
            else:
                result = 'not a number'
        return result
    return wrapper


@get_number_from_message
def get_integer_from_message(text):
    rubles = int(text)

    return rubles


@get_number_from_message
def get_float_from_message(text):
    rubles = int(float(text))
    kopeck = int(round(float(text) % 1, 2) * 100)

    return rubles, kopeck


def create_payment_link(user_id, rubles, kopeck):
    comment = hashlib.shake_128(str(user_id).encode('utf-8') + str(time.time()).encode('utf-8')).hexdigest(8)
    update_variables_cur_payment(user_id, comment)
    payment_link = PAY_LINK.format(rubles, kopeck, comment)

    return payment_link


def check_payment(user_id):
    r = requests.get(url=url_get_history_payed, headers=headers, params={'rows': '20', 'operation': 'IN'})
    data = r.json()['data']
    pay_comment = get_variables_cur_payment(user_id)
    amount = None
    try:
        for i in data:
            if i['comment'] == pay_comment:
                if i['sum']['currency'] == 643:
                    amount = i['sum']['amount']
                elif i['sum']['currency'] == 398:
                    amount = i['sum']['amount'] / 6
                else:
                    amount = None
    except Exception as e:
        print(e)
    else:
        return amount

'''
success_paym_msg = ('💳 Баланс успешно пополнен!\n\n'
                        '+ {0:.2f} 💴 RUB\n'
                        '+ {1:.2f} 💶 EUR')
   
                set_payment_success_in(call.message.chat.id,
                                       amount,
                                       'IN',
                                       datetime.datetime.today().strftime('%Y.%m.%d %H:%M'))
                bot.delete_message(call.message.chat.id,
                                   call.message.message_id)
                bot.send_message(call.message.chat.id,
                                 success_paym_msg.format(in_capital,
                                                         in_energy_user - bns))
                l += float(amount)
                break
    except Exception as e:
        print(e)
    if not l:
        bot.delete_message(call.message.chat.id,
                           call.message.message_id)
        bot.send_message(call.message.chat.id,
                         'Упс! Похоже, деньги еще не зашли! Попробуйте еще раз немного позже :)',
                         reply_markup=types.InlineKeyboardMarkup()
                         .row(types.InlineKeyboardButton('Оплатил!', callback_data='payed')))
'''