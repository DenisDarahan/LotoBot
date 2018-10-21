import sqlite3
from .config import DB_NAME



def create_con():
    con = sqlite3.connect(DB_NAME)
    cur = con.cursor()

    return con, cur


def close_con(con, cur):
    cur.close()
    con.close()



# ==============================================================
# spoof

def get_spoof_active():
    con, cur = create_con()
    result = cur.execute('SELECT active FROM spoof').fetchall()[0][0]
    close_con(con, cur)

    return result


def update_spoof_active(state):
    con, cur = create_con()
    cur.execute('UPDATE spoof SET active = ?', (state,))
    con.commit()
    close_con(con, cur)


def get_spoof_info():
    con, cur = create_con()
    result = cur.execute('SELECT price, prizes, participants FROM spoof').fetchall()[0]
    close_con(con, cur)

    return result


def get_spoof_price():
    con, cur = create_con()
    result = cur.execute('SELECT price FROM spoof').fetchall()[0][0]
    close_con(con, cur)

    return result


def update_spoof_price(price):
    con, cur = create_con()
    cur.execute('UPDATE spoof SET price = ?', (price,))
    con.commit()
    close_con(con, cur)


def get_spoof_prizes():
    con, cur = create_con()
    result = cur.execute('SELECT prizes FROM spoof').fetchall()[0][0]
    close_con(con, cur)

    return result


def update_spoof_prizes(prizes):
    con, cur = create_con()
    cur.execute('UPDATE spoof SET prizes = ?', (prizes,))
    con.commit()
    close_con(con, cur)


def update_spoof_participants():
    con, cur = create_con()
    result = cur.execute('SELECT participants FROM spoof').fetchall()[0][0]
    cur.execute('UPDATE spoof SET participants = ?', (result + 1,))
    con.commit()
    close_con(con, cur)


def clear_spoof():
    con, cur = create_con()
    cur.execute('UPDATE spoof SET active = 0, price = 0, prizes = "", participants = 0')
    con.commit()
    close_con(con, cur)



# ==============================================================
# statistic

def get_statistics_all():
    con, cur = create_con()
    result = cur.execute('SELECT * FROM statistics').fetchall()[0]
    close_con(con, cur)

    return result


def get_statistics_number():
    con, cur = create_con()
    result = cur.execute('SELECT number FROM statistics').fetchall()[0][0]
    close_con(con, cur)

    return result


def update_statistics_number():
    con, cur = create_con()
    result = cur.execute('SELECT number FROM statistics').fetchall()[0][0]
    cur.execute('UPDATE statistics SET number = ?', (result + 1,))
    con.commit()
    close_con(con, cur)


def get_statistics_bank():
    con, cur = create_con()
    result = cur.execute('SELECT bank FROM statistics').fetchall()[0][0]
    close_con(con, cur)

    return result


def update_statistics_end_spoof(bank, profit):
    con, cur = create_con()
    result = cur.execute('SELECT bank, admin_bank FROM statistics').fetchall()[0]
    cur.execute('UPDATE statistics SET bank = ?, admin_bank = ?', (result[0] + bank, result[1] + profit))
    con.commit()
    close_con(con, cur)



# ==============================================================
# user

def create_user(user_id, first_name):
    con, cur = create_con()
    cur.execute('INSERT INTO user(user_id, first_name) VALUES (?, ?)', (user_id, first_name))
    cur.execute('INSERT INTO variables(user_id, stage) VALUES (?, ?)', (user_id, 'user'))
    con.commit()
    close_con(con, cur)


def get_user_first_name(user_id):
    con, cur = create_con()
    result = cur.execute('SELECT first_name FROM user WHERE user_id = ?', (user_id,)).fetchall()[0][0]
    close_con(con, cur)

    return result


def get_user_qiwi_acc(user_id):
    con, cur = create_con()
    result = cur.execute('SELECT qiwi_acc FROM user WHERE user_id = ?', (user_id,)).fetchall()[0][0]
    close_con(con, cur)

    return result


def update_user_qiwi_acc(user_id, qiwi_acc):
    con, cur = create_con()
    result = cur.execute('SELECT qiwi_acc FROM user WHERE user_id = ?', (user_id,)).fetchall()[0][0]
    if qiwi_acc not in result:
        cur.execute('UPDATE user SET qiwi_acc = ? WHERE user_id = ?', (result + qiwi_acc + ' ', user_id))
        con.commit()
    close_con(con, cur)


def delete_user_qiwi_acc(user_id, qiwi_acc):
    con, cur = create_con()
    result = cur.execute('SELECT qiwi_acc FROM user WHERE user_id = ?', (user_id,)).fetchall()[0][0]
    cur.execute('UPDATE user SET qiwi_acc = ? WHERE user_id = ?', (result.replace(qiwi_acc + ' ', ''), user_id))
    con.commit()
    close_con(con, cur)



# ==============================================================
# variables

def get_variables_stage(user_id):
    con, cur = create_con()
    result = cur.execute('SELECT stage FROM variables WHERE user_id = ?', (user_id,)).fetchall()[0][0]
    close_con(con, cur)

    return result


def update_variables_stage(user_id, stage):
    con, cur = create_con()
    cur.execute('UPDATE variables SET stage = ? WHERE user_id = ?', (stage, user_id))
    con.commit()
    close_con(con, cur)


def get_variables_amount(user_id):
    con, cur = create_con()
    result = cur.execute('SELECT amount FROM variables WHERE user_id = ?', (user_id,)).fetchall()[0][0]
    close_con(con, cur)

    return result


def update_variables_amount(user_id, amount):
    con, cur = create_con()
    result = cur.execute('SELECT amount FROM variables WHERE user_id = ?', (user_id,)).fetchall()[0][0]
    cur.execute('UPDATE variables SET amount = ? WHERE user_id = ?', (result + amount, user_id))
    con.commit()
    close_con(con, cur)

    return result + amount


def get_variables_activity(user_id):
    con, cur = create_con()
    result = cur.execute('SELECT activity FROM variables WHERE user_id = ?', (user_id,)).fetchall()[0][0]
    close_con(con, cur)

    return result


def update_variables_activity(user_id):
    con, cur = create_con()
    result = cur.execute('SELECT activity FROM variables WHERE user_id = ?', (user_id,)).fetchall()[0][0]
    cur.execute('UPDATE variables SET activity = ? WHERE user_id = ?', (result + 1, user_id))
    con.commit()
    close_con(con, cur)


def get_variables_private_room_info(user_id):
    con, cur = create_con()
    result = cur.execute('SELECT amount, activity FROM variables WHERE user_id = ?', (user_id,)).fetchall()[0]
    close_con(con, cur)

    return result


def get_variables_cur_payment(user_id):
    con, cur = create_con()
    result = cur.execute('SELECT cur_payment FROM variables WHERE user_id = ?', (user_id,)).fetchall()[0][0]
    close_con(con, cur)

    return result


def update_variables_cur_payment(user_id, comment):
    con, cur = create_con()
    cur.execute('UPDATE variables SET cur_payment = ? WHERE user_id = ?', (comment, user_id))
    con.commit()
    close_con(con, cur)


def get_variables_cur_activity(user_id):
    con, cur = create_con()
    result = cur.execute('SELECT cur_activity FROM variables WHERE user_id = ?', (user_id,)).fetchall()[0][0]
    close_con(con, cur)

    return result


def get_variables_users_by_cur_activity(state):
    con, cur = create_con()
    result = cur.execute('SELECT user_id FROM variables WHERE cur_activity = ?', (state,)).fetchall()
    close_con(con, cur)

    return result


def update_variables_cur_activity(user_id, state):
    con, cur = create_con()
    cur.execute('UPDATE variables SET cur_activity = ? WHERE user_id = ?', (state, user_id))
    con.commit()
    close_con(con, cur)


def clear_variables_cur_activity():
    con, cur = create_con()
    cur.execute('UPDATE variables SET cur_activity = 0')
    con.commit()
    close_con(con, cur)
