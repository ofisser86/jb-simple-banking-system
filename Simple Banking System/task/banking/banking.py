# Write your code here
import sys
import sqlite3
from random import sample
database = "card.s3db"


def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Exception as e:
        print(e)

    return conn


def create_table(conn, create_table_sql):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Exception as e:
        print(e)


def update_card(conn, card):
    """
    Create a new task
    :param conn:
    :param card:
    :return:
    """

    sql = """INSERT INTO Card(number, pin)
              VALUES({card}, {PIN})""".format(card=card['card_number'], PIN=card['PIN'])
    cur = conn.cursor()
    cur.execute(sql)
    conn.commit()
    return cur.lastrowid


def create_card():
    card = {}
    bin_number = "".join([str(n) for n in sample(range(9), 9)])
    luhn = [int(i) for i in '400000' + str(bin_number)]
    luhn[::2] = [2 * x for x in luhn[::2]]
    for i in range(len(luhn)):
        if luhn[i] > 9:
            luhn[i] -= 9

    if sum(luhn) % 10 == 0:
        checksum = 0
    else:
        checksum = 10 - sum(luhn) % 10

    card_number = '400000' + str(bin_number) + str(checksum)
    pin = ''.join([str(n) for n in sample(range(9), 4)])
    card['card_number'] = int(card_number)
    card['PIN'] = int(pin)
    card['balance'] = 0

    sql_create_card_table = """CREATE TABLE IF NOT EXISTS Card (
                        id INTEGER AUTOINCREMENT,
                        number TEXT,
                        pin TEXT,
                        balance INTEGER DEFAULT 0
                    );"""

    # create a database connection
    conn = create_connection(database)

    # create tables
    if conn is not None:
        # create projects table
        create_table(conn, sql_create_card_table)
        update_card(conn, card)
    else:
        print("Error! cannot create the database connection.")

    return card


def get_all_from_card(conn):
    """
        Query all rows in the tasks table
        :param conn: the Connection object
        :return:
        """
    cur = conn.cursor()
    cur.execute("SELECT * FROM Card")

    rows = cur.fetchall()

    return rows


def user_account(check_card_number, check_card_pin):
    if check_card_number in temp_store and check_card_pin in temp_store:
        print()
        print('You have successfully logged in!')
        print()
    else:
        return "Wrong card number or PIN!"

    while True:
        sub_menu_option = int(input("1. Balance\n2. Log out\n0. Exit\n"))
        print()
        if sub_menu_option == 1:
            print(f"Balance: {user_card['balance']}")
            print()
        elif sub_menu_option == 2:
            return "You have successfully logged out!"
        elif sub_menu_option == 0:
            sys.exit()


while True:
    menu_option = int(input("1. Create an account\n2. Log into account\n0. Exit\n"))
    print()
    if menu_option == 1:
        user_card = create_card()
        connection = create_connection(database)
        all_cards = get_all_from_card(connection)
        user_card_number = user_card['card_number']
        user_card_pin = user_card['PIN']
        user_card_balance = user_card['balance']
        # temp_store.extend([user_card_number, user_card_pin, user_card_balance])
        print('Your card has been created')
        print(f"Your card number:\n{user_card_number}\nYour card PIN:\n{user_card_pin}")
    elif menu_option == 2:
        validate_card_number = int(input("Enter your card number:\n"))
        validate_card_pin = int(input("Enter your PIN:\n"))
        print(user_account(validate_card_number, validate_card_pin))
    elif menu_option == 0:
        print('Bye!')
        break
    print()
