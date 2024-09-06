import sqlite3

connection = sqlite3.connect('db_for_hmw.db')
cursor = connection.cursor()
cursor.execute('''
CREATE TABLE IF NOT EXISTS Products(
id INTEGER PRIMARY KEY,
title TEXT NOT NULL,
description TEXT,
price INTEGER NOT NULL
);
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS Users(
id INTEGER PRIMARY KEY,
username TEXT NOT NULL,
email TEXT NOT NULL,
age INT NOT NULL,
balance INT NOT NULL
);
''')


def adder():
    for i in range(1, 5):
        cursor.execute('INSERT INTO Products(title, description, price) VALUES (?, ?, ?)',
                       (f'Продукт {i}',
                        f'Описание {i}', f'{i * 100}'))
        connection.commit()


# adder()


def add_user(username, email, age):
    cursor.execute('INSERT INTO Users(username, email, age, balance) VALUES (?, ?, ?, ?)',
                   (f'{username}', f'{email}', f'{age}', 1000))
    connection.commit()


def is_included(username):
    check_user = cursor.execute('SELECT * FROM Users WHERE username=?', (username,))
    if check_user.fetchone() is not None:
        return True
    else:
        return False


def get_all_products():
    cursor.execute('SELECT * FROM Products')
    products_list = cursor.fetchall()
    return products_list


# connection.commit()
# connection.close()
