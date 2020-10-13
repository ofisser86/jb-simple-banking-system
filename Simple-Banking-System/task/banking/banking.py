import os
import sqlite3

from random import randint


# Define path for store rating in rating txt
ABS_PATH = os.path.abspath(__file__)
BASE_DIR = os.path.dirname(ABS_PATH)
DATABASE = os.path.join(BASE_DIR, 'card.s3db')

def prRed(skk): return "\033[31m {}\033[00m" .format(skk)
def prGreen(skk): return "\033[92m {}\033[00m" .format(skk) 
def prYellow(skk): return "\033[93m {}\033[00m" .format(skk)
def prCyan(skk): return "\033[96m {}\033[00m" .format(skk)
def prOrange(skk): return "\033[33m {}\033[00m" .format(skk)


class Bank:
    # Create connection to DB, start the App menu
    def __init__(self):
        self.logged_in = False
        self.conn = sqlite3.connect(DATABASE)
        self.cur = self.conn.cursor()
        self.create_table()
        self.current_card = None
        self.menu()

    def create_table(self):
        sql_create_card_table = """CREATE TABLE IF NOT EXISTS card (id INTEGER, number TEXT,
        pin TEXT, balance INTEGER DEFAULT 0); """
        self.cur.execute(sql_create_card_table)
        self.conn.commit()

    def create_card(self, id_, number, pin, balance):
        sql_insert_card = """INSERT INTO card (id, number, pin, balance) VALUES (?, ?, ?, ?); """
        data_tuple = (id_, number, pin, balance)
        self.cur.execute(sql_insert_card, data_tuple)
        self.conn.commit()

    # Get card id
    def gen_id(self):
        query = """SELECT id FROM card ORDER BY id DESC LIMIT 1;"""
        self.cur.execute(query)
        records = self.cur.fetchall()
        try:
            return records[0][0] + 1
        except IndexError:
            return 1

    # Get all cards
    def get_all_cards(self):
        query = """SELECT number FROM card"""
        self.cur.execute(query)
        rows = self.cur.fetchall()
        return rows

    # Card validation
    def check_card(self, transfer_to_card):
        query = f"""SELECT number FROM card WHERE number = {transfer_to_card}"""
        self.cur.execute(query)

        luhn = [int(i) for i in transfer_to_card[:-1]]
        luhn[::2] = [2 * x for x in luhn[::2]]
        for i in range(len(luhn)):
            if luhn[i] > 9:
                luhn[i] -= 9

        checksum = int(transfer_to_card[len(transfer_to_card) - 1])
        card = self.cur.fetchone()
        if (sum(luhn) + checksum) % 10 != 0:
            print(prRed('Attention! ') + "Probably you made a mistake in the card number. Please try again!\n")
            self.account_menu()
        elif card is None:
            print("Such card does not exist.\n")
            self.account_menu()
        elif self.current_card == transfer_to_card:
            print(prRed('Attention! ') + "You can't transfer money to the same account! Please try again!\n")
            self.account_menu()

    def read_card(self, card, pin):
        query = """SELECT number, pin FROM card WHERE number = ? AND pin = ?"""
        data_tuple = (card, pin)
        self.cur.execute(query, data_tuple)
        rows = self.cur.fetchone()
        return rows

    def menu(self):
        while not self.logged_in:
            print('1.' + prGreen('Create an account\n') + '2. Log into account\n0.' + prRed('Exit'))
            choice = input('>')
            if choice == '1':
                self.create()
            elif choice == '2':
                self.login()
            elif choice == '0':
                print('\nBye!')
                self.cur.close()
                self.conn.close()
                quit()
    
    # Account menu
    def account_menu(self):
        while self.logged_in:
            print('1. Balance\n2.' + prCyan('Add income\n') + '3. Do transfer\n4.' + prYellow('Close account\n') + '5. Log out\n0.' + prRed('Exit'))
            choice = input()
            if choice == '1':
                balance = self.get_balance()
                print(f'\nBalance: {balance}\n')
            elif choice == '2':
                print("\nEnter income:")
                income = int(input())
                self.add_income(income)
                print(prGreen('Success! ') + 'Income was added!\n')
            elif choice == '3':
                print('\nTransfer')
                transfer_to_card = input("Enter card number:\n")
                self.check_card(transfer_to_card)
                money_to_transfer = int(input("Enter how much money you want to transfer:\n"))
                print(self.do_transfer(transfer_to_card, money_to_transfer))
            elif choice == '4':
                try:
                    self.close_account()
                    print("\nThe account has been closed!\n")
                    self.logged_in = False
                    self.current_card = None
                except Exception as e:
                    print(e)
            elif choice == '5':
                self.logged_in = False
                print('\nYou have ' + prGreen('successfully') + 'logged out!\n')
            elif choice == '0':
                print('\nBye!')
                self.cur.close()
                self.conn.close()
                quit()

    # Create card with Luhn algorythm
    def create(self):
        print()
        id_ = self.gen_id()
        card = self.luhn_alg()
        pin = str.zfill(str(randint(0000, 9999)), 4)
        self.create_card(id_, card, pin, 0)
        print('Your card has been created\nYour card number:\n' + prOrange(f'{card}') + f'\nYour card PIN:\n{pin}\n')

    # Login to user account
    def login(self):
        print('\nEnter your card number:')
        card = input()
        print('Enter your PIN:')
        pin = input()
        cards = self.read_card(card, pin)
        if cards:
            print('\nYou have successfully logged in!\n')
            self.logged_in = True
            self.current_card = card
            self.account_menu()
        else:
            print(pr(Red('\nAttention!')) + 'Wrong card number or Pin! Try again!\n')
    
    # Get the card balance
    def get_balance(self):
        query = f"""SELECT balance FROM card WHERE number = {self.current_card};"""
        balance = self.cur.execute(query)
        return balance.fetchone()[0]

    # Fill the card
    def add_income(self, income):
        updated_balance = self.get_balance() + income
        query = f"""UPDATE card SET balance = {updated_balance} WHERE number = {self.current_card}"""
        self.cur.execute(query)
        self.conn.commit()

    # Make money transfer from card to card
    def do_transfer(self, transfer_to_card, money_to_transfer):
        card_balance = self.get_balance()
        query = f"""BEGIN TRANSACTION;
                    UPDATE card
                       SET balance = balance - {money_to_transfer}
                    WHERE number = {self.current_card};
                    
                    UPDATE card
                       SET balance = balance + {money_to_transfer}
                    WHERE number = {transfer_to_card};
                    COMMIT;
                  """
        if card_balance >= money_to_transfer and card_balance != 0:
            self.cur.executescript(query)
            self.conn.commit()
            return prGreen("Success!\n")
        else:
            return 'Not enough money!'

    # Delete card from database
    def close_account(self):
        query = f"""DELETE FROM card WHERE number = {self.current_card};"""
        self.cur.execute(query)
        self.conn.commit()
        self.current_card = None

    # Luhn algorythm for creating the valid card
    def luhn_alg(self):
        card = '400000' + str.zfill(str(randint(000000000, 999999999)), 9)
        card_check = [int(i) for i in card]
        for index, _ in enumerate(card_check):
            if index % 2 == 0:
                card_check[index] *= 2
            if card_check[index] > 9:
                card_check[index] -= 9
        check_sum = str((10 - sum(card_check) % 10) % 10)
        card += check_sum
        return card


if __name__ == '__main__':
    stage_4 = Bank()


