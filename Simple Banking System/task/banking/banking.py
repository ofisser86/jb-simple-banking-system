# Write your code here
import sys
from random import sample

temp_store = []


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
    return card


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
        user_card_number = user_card['card_number']
        user_card_pin = user_card['PIN']
        user_card_balance = user_card['balance']
        temp_store.extend([user_card_number, user_card_pin, user_card_balance])
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
