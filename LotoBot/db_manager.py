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
# user

def create_user(user_id, first_name):
    con, cur = create_con()
    cur.execute('INSERT INTO user(user_id, first_name) VALUES (?, ?)', (user_id, first_name))
    cur.execute('INSERT INTO variables(user_id, stage) VALUES (?, ?)', (user_id, 'user'))
    con.commit()
    close_con(con, cur)




# ==============================================================
# variables

def get_variables_stage(user_id):
    con, cur = create_con()
    result = cur.execute('SELECT stage FROM variables WHERE user_id = ?', (user_id,))
    close_con(con, cur)

    return result


def set_variables_stage(user_id):
    con, cur = create_con()
    cur.execute('SELECT stage FROM variables WHERE user_id = ?', (user_id,))
    con.commit()
    close_con(con, cur)