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
# statistic

def get_statistic_all():
    con, cur = create_con()
    result = cur.execute('SELECT * FROM statistics').fetchall()[0]
    close_con(con, cur)

    return result



# ==============================================================
# user

def create_user(user_id, first_name):
    con, cur = create_con()
    cur.execute('INSERT INTO user(user_id, first_name) VALUES (?, ?)', (user_id, first_name))
    cur.execute('INSERT INTO variables(user_id, stage) VALUES (?, ?)', (user_id, 'user'))
    con.commit()
    close_con(con, cur)


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
