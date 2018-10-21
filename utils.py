import re
import time
import hashlib
import requests
import json
from random import choice

from LotoBot.config import PAY_LINK, url, url_get_history_payed, headers
from LotoBot.db_manager import *



def get_number_from_message(func):
    def wrapper(text):
        try:
            result = func(text)
        except:
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


@get_number_from_message
def get_qiwi_acc_from_message(text):
    if len(text) == 12:
        qiwi_acc = re.match('^\+\d\d\d\d\d\d\d\d\d\d\d', text).group()
    else:
        qiwi_acc = re.match('^\+\d\d\d\d\d\d\d\d\d\d\d\d', text).group()

    return qiwi_acc


def withdraw_money_from_account(amount, qiwi_acc):
    data = ('{"id":"1","sum":{"amount":"def","currency":"643"},'
            '"paymentMethod":{"type":"Account","accountId":"643"},'
            '"comment":"def","fields":{"account":"def"}}')
    js = json.loads(data)
    js["id"] = str(int(time.time()) * 1000)
    js['sum']['amount'] = str(amount)
    js['comment'] = 'Вывод средств'
    js['fields']['account'] = qiwi_acc
    data = json.dumps(js)
    r = requests.post(url=url, data=data, headers=headers)
    try:
        if r.json()['transaction']['state']['code'] == 'Accepted':
            return True
    except KeyError:
        return r.json()['message']

    return None


def convert_info_to_string(pattern, info_list):
    number_winners = len(info_list[0])
    prizes_string = ''
    if number_winners == 1:
        prizes_string = pattern.format(*[j[0] for j in info_list])
        return prizes_string
    else:
        for i in range(number_winners):
            prizes_string += str(i + 1) + ') ' + pattern.format(*[j[i] for j in info_list])
        return prizes_string


def get_winners(number_winners):
    winners = []
    possible_winners = [i[0] for i in get_variables_users_by_cur_activity(1)]
    for i in range(number_winners):
        winner = choice(possible_winners)
        winners.append(winner)
        possible_winners.remove(winner)

    return winners


def get_spoof_info_for_message(mode):
    number = get_statistics_number()
    price, prizes, participants = get_spoof_info()
    prizes = [int(i) for i in prizes.split()]

    # User Interface -> Розыгрыши
    if mode == 4:
        return number, price, prizes[0]

    else:
        profit = 100 - sum(prizes)
        bank = price * participants

        # Admin Interface -> Розыгрыш -> Создать новый розыгрыш
        if mode == 1:
            pattern = '{}% от банка\n'
            prizes_string = convert_info_to_string(pattern, [prizes])
            return number + 1, profit, price, prizes_string

        # Admin Interface -> Розыгрыш -> Текущий розыгрыш
        elif mode == 2:
            real_profit = bank * profit / 100
            pattern = '{} руб ({}%)\n'
            prizes_string = convert_info_to_string(pattern, [[int(i * bank / 100) for i in prizes], prizes])
            return number, participants, bank, real_profit, profit, price, prizes_string

        # Admin Interface -> Розыгрыш -> Завершить розыгрыш
        elif mode == 3:
            winners = get_winners(len(prizes))
            pattern = '{} <a href="tg://user?id={}">{}</a> {} руб\n'
            l = ['🥇', '🥈', '🥉', *['🎗' for _ in range(len(prizes) - 3)]]
            winners_by_name = [get_user_first_name(i) for i in winners]
            real_prizes = [int(i * bank / 100) for i in prizes]
            winners_string = convert_info_to_string(pattern, [l, winners, winners_by_name, real_prizes])
            return winners_string

        else:
            raise IndexError


@get_number_from_message
def get_prizes_list_from_message(text):
    prizes = text.split()
    if sum([int(i) for i in prizes]) > 100:
        raise ValueError
    else:
        return text
