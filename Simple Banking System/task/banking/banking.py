# Write your code here
import  sys
import random

temp_store = []


def create_card():
    card = {}
    card_number = '400000' + str(random.randint(0, 9999999999))
    pin = random.randint(1000, 9999)
    card['card_number'] = int(card_number)
    card['PIN'] = pin
    return card


while True:
    menu_option = int(input("1. Create an account\n2. Log into account\n0. Exit\n"))
    print()
    if menu_option == 1:
        user_card = create_card()['card_number']
        user_card_pin = create_card()['PIN']
        temp_store += [user_card, user_card_pin]
        print('Your card has been created')
        print(f"Your card number:\n{user_card}\nYour card PIN:\n{user_card_pin}")
    elif menu_option == 2:
        validate_card_number = int(input("Enter your card number:\n"))
        validate_card_pin = int(input("Enter your PIN:\n"))
        if validate_card_number in temp_store and validate_card_pin in temp_store:
            print()
            print('You have successfully logged in!')
            print()
            sub_menu_option = ''
            while sub_menu_option != 2:
                sub_menu_option = int(input("1. Balance\n2. Log out\n0. Exit\n"))
                print()
                if sub_menu_option == 1:
                    balance = 0
                    print(f"Balance: {balance}")
                    print()
                elif sub_menu_option == 2:
                    print("You have successfully logged out!")
                elif sub_menu_option == 0:
                    sys.exit()

        else:
            print("Wrong card number or PIN!")
    elif menu_option == 0:
        print('Bye!')
        break
    print()
