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


def get_qiwi_acc(user_id):
    qiwi_acc = get_user_qiwi_acc(user_id).split()
    if qiwi_acc == []:
        return None
    else:
        return qiwi_acc
'''
    try:
        if len(message.text) == 12:
            phone = re.match('^\+\d\d\d\d\d\d\d\d\d\d\d', message.text).group()
        else:
            phone = re.match('^\+\d\d\d\d\d\d\d\d\d\d\d\d', message.text).group()
        set_user_stage(message.chat.id, '')
        money = int(get_user_cache(message.chat.id))
        cash_out = money / 10
        energy_out = money / 100
        data = '{"id":"1","sum":{"amount":"def","currency":"643"},' \
               '"paymentMethod":{"type":"Account","accountId":"643"},' \
               '"comment":"def","fields":{"account":"def"}}'
        js = json.loads(data)
        js["id"] = str(int(time.time()) * 1000)
        js['sum']['amount'] = str(cash_out)
        js['comment'] = 'Вывод средств'
        js['fields']['account'] = '+' + phone
        data = json.dumps(js)
        r = requests.post(url=url, data=data, headers=headers)
        create_payment(message.chat.id, 'Вывод средств', 'OUT', phone)
        try:
            if r.json()['transaction']['state']['code'] == 'Accepted':
                set_payment_success_out(message.chat.id, cash_out, 'OUT',
                                    datetime.datetime.today().strftime('%Y.%m.%d %H:%M'),
                                    money, energy_out)
                bot.send_message(383053151,
                                 'Вывод!\n'
                                 'ID: {0}\n'
                                 'Sum: {1}'.format(message.chat.id,
                                                   cash_out))
                bot.send_message(message.chat.id,
                                 'Поздравляем!\n'
                                 'Вы вывели свои заработанные деньги 😍💰\n\n'
                                 '✅ Перечислено: {0} руб\n\n'
                                 'Ждём тебя за следующим выводом😉'.format(cash_out),
                                 reply_markup=main_menu())
        except KeyError:
            bot.send_message(message.chat.id,
                             'Ошибка транзакции! {0}'.format(r.json()['message']))
    except AttributeError:
        bot.send_message(message.chat.id,
                         'Пожалуйста, введите номер формата +70001111111')                     
'''