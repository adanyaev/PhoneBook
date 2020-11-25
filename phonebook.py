import os
import sqlite3
from prettytable import PrettyTable
from time import sleep


class PhoneBook():

    def __init__(self, path=None):
        if path is None:
            path = "contacts.db"
        self.conn = sqlite3.connect(path)
        self.cursor = self.conn.cursor()
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS phonebook
                  (name text, surname text, mobile text,
                   working text, home text, birthdate text)
               """)
        self.conn.commit()


    def get_contact(self, name, surname):
        self.cursor.execute("SELECT * FROM phonebook WHERE name=? AND surname=?", [name, surname])
        return self.cursor.fetchone()

    def create_contact(self, name, surname):
        if self.get_contact(name, surname):
            return False
        self.cursor.execute("INSERT INTO phonebook(name, surname) VALUES (?, ?)", [name, surname])
        self.conn.commit()
        return True

    def add_number(self, name, surname, category, number):
        self.cursor.execute("SELECT {} FROM phonebook WHERE name=? AND surname=?".format(category), [name, surname])
        nums = self.cursor.fetchone()[0]
        nums = nums + ', {}'.format(number) if nums else number
        self.cursor.execute("UPDATE phonebook SET {}='{}' WHERE name=? AND surname=?".format(category, nums), [name, surname])
        self.conn.commit()


    def add_date(self, name, surname, date):
        self.cursor.execute("UPDATE phonebook SET birthdate='{}' WHERE name=? AND surname=?".format(date), [name, surname])
        self.conn.commit()

    def __str__(self):
        self.cursor.execute("SELECT * FROM phonebook")
        data = self.cursor.fetchall()
        x = PrettyTable()
        x.field_names = ['name', 'surname', 'mobile', 'working', 'home', 'date']
        x.add_rows(data)
        return str(x)

    @staticmethod
    def check_number(number):
        return True

    @staticmethod
    def check_date(date):
        return True


book = PhoneBook()

while True:
    print('''
########  ######## ######## #######    #######   #######  ##    ## 
##     ## ##       ##       ##     ## ##     ## ##     ## ##   ##  
##     ## ##       ##       ##     ## ##     ## ##     ## ##  ##   
########  ######   ######   ########  ##     ## ##     ## #####    
##   ##   ##       ##       ##     ## ##     ## ##     ## ##  ##   
##    ##  ##       ##       ##     ## ##     ## ##     ## ##   ##  
##     ## ######## ##       #######    #######   #######  ##    ##  by Artem Danyaev
''')
    print(
        '''Enter command number:
        (1) Add new contact
        (2) Print phonebook
        (3) gsdlgjsdjgs''')
    command = input().strip()
    if command == '1':
        while True:
            name = input('Enter name: ')
            surname = input('Enter surname: ')
            ret = True
            if book.get_contact(name, surname):
                print("This contact already exists. You can edit him (1), enter new name (2) or go back to menu (3)")
                while True:
                    command = input()
                    if command == "1":
                        command = "Номер команды на редактирование"
                        ret = True
                        break
                    elif command == "2":
                        command = "1"
                        ret = False
                        break
                    elif command == "3":
                        command = "back"
                        ret = True
                        break
                    else:
                        print("Incorrect input. Try again: ")
            if ret:
                break

        if command == 'back':
            continue

        book.create_contact(name, surname)

        while True:
            print('''Choose number category:
				(1) Mobile
				(2) Working
				(3) Home''')

            while True:
                category = input()
                if category == '1':
                    category = 'mobile'
                    break
                elif category == '2':
                    category = 'working'
                    break
                elif category == '3':
                    category = 'home'
                    break
                else:
                    print("Incorrect input")

            while True:
                number = input("Enter number: ")
                if PhoneBook.check_number(number):
                    break
                print("incorrect input. Try again")

            if number[0] == '+':
                number = '8' + number[2:]

            book.add_number(name, surname, category, number)

            while True:
                com = input("Add additional number? (1) for YES, (2) for NO:")
                if com == '1':
                    ret = True
                    break
                if com == '2':
                    ret = False
                    break
                print("Incorrect input. Try again")

            if ret == True:
                continue
            break

        print("Add date of birth in this format \"dd.mm.yy\" or print \"skip\" to skip")
        while True:
            com = input()
            if com == "skip":
                break
            elif PhoneBook.check_date(com):
                book.add_date(name, surname, com)
                break
            print("Incorrect input. Try again")

        print("New contact created")
        sleep(1)
        os.system('cls' if os.name == 'nt' else 'clear')
        continue

    if command == '2':
        os.system('cls' if os.name == 'nt' else 'clear')
        print(book)
        print("Print \"back\" to return to menu")
        while True:
            c = input()
            if c == 'back':
                break

    if command == '3':
        pass
