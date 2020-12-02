from phonebook import PhoneBook
import os
import sys
from time import sleep

book = PhoneBook()

skip = False
skip_input = False

while True:
    if not skip:
        os.system('cls' if os.name == 'nt' else 'clear')
        print('''
########  ######## ######## #######    #######   #######  ##    ## 
##     ## ##       ##       ##     ## ##     ## ##     ## ##   ##  
##     ## ##       ##       ##     ## ##     ## ##     ## ##  ##   
########  ######   ######   ########  ##     ## ##     ## #####    
##   ##   ##       ##       ##     ## ##     ## ##     ## ##  ##   
##    ##  ##       ##       ##     ## ##     ## ##     ## ##   ##  
##     ## ######## ##       #######    #######   #######  ##    ##  by Artem Danyaev
''')
        print('''Enter command number:
(1) Add new contact
(2) Print phonebook
(3) Edit contact
(4) Find contacts
(5) Delete contact by name and surname
(6) Delete contact by number
(7) Find out age of contact
(8) See contacts with birtday in the next 30 days
(9) Sort contacts by age''')
    if not skip_input:
        command = input()
    skip_input = False
    skip = False
    if command == '1':
        while True:
            while True:
                name = input('Enter name: ')
                if PhoneBook.check_name(name):
                    break
                print("Incorrect input. Try again")
            while True:
                surname = input('Enter surname: ')
                if PhoneBook.check_name(surname):
                    break
                print("Incorrect input. Try again")

            ret = True
            if book.get_contacts(name, surname):
                print("This contact already exists. You can edit him (1), enter new name (2) or go back to menu (3)")
                while True:
                    com = input()
                    if com == "1":
                        command = "3"
                        skip = True
                        skip_input = True
                        ret = 'back'
                        break
                    elif com == "2":
                        ret = False
                        break
                    elif com == "3":
                        ret = 'back'
                        break
                    else:
                        print("Incorrect input. Try again: ")
            if ret:
                break
        if ret == 'back':
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
                number = input("Enter number starting from +7 or 8:")
                if PhoneBook.check_number(number):
                    break
                print("incorrect input. Try again")

            if number[0] == '+':
                number = '8' + number[2:]

            book.add_number(name, surname, category, number)

            while True:
                com = input("Add additional number? (1) for YES, (2) for NO: ")
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
        os.system('cls' if os.name == 'nt' else 'clear')
        print("New contact created")
        sleep(1)
        os.system('cls' if os.name == 'nt' else 'clear')
        continue


    elif command == '2':
        os.system('cls' if os.name == 'nt' else 'clear')
        print(book)
        print("Print \"back\" to return to menu")
        while True:
            c = input()
            if c == 'back':
                break

    elif command == '3':
        os.system('cls' if os.name == 'nt' else 'clear')
        while True:
            print(
                "Enter name and surname of the contact, print \"all\" to see all contacts or \"back\" to go back to menu")
            s = input()
            if s == "all":
                os.system('cls' if os.name == 'nt' else 'clear')
                print(book)
                continue
            if s == "back":
                break
            if len(s.split(' ')) != 2 or s.split(' ')[1] == '':
                print("Wrong input. try again")
                continue

            name, surname = s.split(' ')
            if not book.get_contacts(name, surname):
                print("Contacts not found. Try again")
                continue

            os.system('cls' if os.name == 'nt' else 'clear')

            while True:
                book.print_contacts(book.get_contacts(name, surname))
                print('''Enter the number of field that you want to edit:
(1) Name
(2) Surname
(3) Mobile phones
(4) Working phones
(5) Home phones
(6) Date of birth
(7) Edit another contact
(8) back to menu''')
                com = input()
                if com == '1':
                    while True:
                        newname = input("Enter new name: ")
                        if not PhoneBook.check_name(newname):
                            print("Incorrect name. Try again")
                            continue
                        if book.get_contacts(name=newname, surname=surname):
                            print("Contact with these name and surname already exists. Try again")
                            continue
                        break
                    book.edit_contact(name, surname, newname=newname)
                    name = newname
                    os.system('cls' if os.name == 'nt' else 'clear')
                    print("Contact successfully edited")
                    continue

                if com == '2':
                    while True:
                        newsurname = input("Enter new surname: ")
                        if not PhoneBook.check_name(newsurname):
                            print("Incorrect surname. Try again")
                            continue
                        if book.get_contacts(name=name, surname=newsurname):
                            print("Contact with these name and surname already exists. Try again")
                            continue
                        break
                    book.edit_contact(name, surname, newsurname=newsurname)
                    surname = newsurname
                    os.system('cls' if os.name == 'nt' else 'clear')
                    print("Contact successfully edited")
                    continue

                elif com == '3' or com == '4' or com == '5':
                    cats = ['mobile', 'working', 'home']
                    cat = int(com) - 3
                    nums = book.get_contacts(name, surname)[0][cat + 2]

                    if not nums:
                        print("{} {} does not have {} numbers yet".format(name, surname, cats[cat]))
                        print("Enter new number starting from +7 or 8:")
                        while True:
                            number = input()
                            if PhoneBook.check_number(number):
                                break
                            print("Incorrect input. Try again")
                        if number[0] == '+':
                            number = '8' + number[2:]
                        book.add_number(name, surname, cats[cat], number)
                        os.system('cls' if os.name == 'nt' else 'clear')
                        print("New number successfully added")
                        continue

                    nums = nums.split(', ')
                    s = "{} {}`s {} numbers:\n".format(name, surname, cats[cat])
                    for i in range(len(nums)):
                        s += "({}) {}\n".format(i + 1, nums[i])
                    s += "({}) Add new number".format(len(nums) + 1)
                    print(s)
                    print("Enter the number of phone that you want to replace or delete")
                    while True:
                        opt = input()
                        opts = [str(i) for i in range(1, len(nums) + 2)]
                        if opt not in opts:
                            print("Wrong input. Try again")
                            continue
                        break
                    opt = int(opt) - 1

                    if opt == len(nums):
                        print("Enter new number starting from +7 or 8:")
                        while True:
                            number = input()
                            if PhoneBook.check_number(number):
                                break
                            print("Incorrect input. Try again")
                        if number[0] == '+':
                            number = '8' + number[2:]
                        book.add_number(name, surname, cats[cat], number)
                        os.system('cls' if os.name == 'nt' else 'clear')
                        print("New number successfully added")
                        continue

                    print(
                        "{} is chosen. Enter new number (starting from +7 or 8) or type \"delete\" to delete it:".format(
                            nums[opt]))
                    while True:
                        num = input()
                        if not PhoneBook.check_number(num) and num != 'delete':
                            print("Wrong input. Try again")
                            continue
                        break
                    if num == 'delete':
                        nums.pop(opt)
                    else:
                        if num[0] == '+':
                            num = '8' + num[2:]
                        nums[opt] = num
                    book.add_numbers(name, surname, cats[cat], nums)
                    os.system('cls' if os.name == 'nt' else 'clear')
                    print("Number successfully changed" if num != 'delete' else "Number successfully deleted")
                    continue

                elif com == '6':
                    while True:
                        newdate = input("Enter new date in this format \"dd.mm.yyyy\": ")
                        if not PhoneBook.check_date(newdate):
                            print("Incorrect date. Try again")
                            continue
                        break
                    book.add_date(name, surname, newdate)
                    os.system('cls' if os.name == 'nt' else 'clear')
                    print("Date successfully edited")
                    continue
                elif com == '7':
                    ret = False
                    os.system('cls' if os.name == 'nt' else 'clear')
                    break
                elif com == '8':
                    ret = True
                    os.system('cls' if os.name == 'nt' else 'clear')
                    break
                else:
                    os.system('cls' if os.name == 'nt' else 'clear')
                    print("Wrong input. Try again")
                    continue
                break
            if ret:
                break

    elif command == '4':
        os.system('cls' if os.name == 'nt' else 'clear')

        while True:
            name = input("Enter name or type \"skip\" if name doesn`t matter: ")
            if name == "skip":
                break
            if not PhoneBook.check_name(name):
                print("Wrong input. Try again")
                continue
            break
        while True:
            surname = input("Enter surname or type \"skip\" if surname doesn`t matter: ")
            if surname == "skip":
                break
            if not PhoneBook.check_name(surname):
                print("Wrong input. Try again")
                continue
            break
        contacts = book.get_contacts(name if name != "skip" else None, surname if surname != "skip" else None)
        if contacts:
            book.print_contacts(contacts)
        else:
            print("Contacts were not found")
            print("Press any key to continue")
            sys.stdin.read(1)
            os.system('cls' if os.name == 'nt' else 'clear')
            continue
        while True:
            print("Enter the number or the list of numbers (starting from 8 or +7) comma separated or type \"skip\":")
            nums = input()
            if nums != 'skip':
                nums = [i.strip() for i in nums.split(',')]
                for i in nums:
                    if not PhoneBook.check_number(i):
                        print("incorrect input. Try again")
                        continue
                    else:
                        if i[0] == '+':
                            i = '8' + i[2:]
                contacts1 = contacts[:]
                for i in contacts1:
                    for j in nums:
                        if not (i[2].find(j) != -1 or i[3].find(j) != -1 or i[4].find(j) != -1):
                            contacts.remove(i)
                            break
                break
            else:
                break
        if not contacts:
            print("Contacts were not found")
            print("Press any key to continue")
            sys.stdin.read(1)
            os.system('cls' if os.name == 'nt' else 'clear')
            continue
        while True:
            print("Enter date in this \"dd.mm.yyyy\" or this \"dd.mm\" formats or print \"skip\":")
            date = input()
            if date != 'skip':
                if not PhoneBook.check_date(date if len(date) > 5 else date + '.2000'):
                    print("Incorrect date. Try again")
                    continue
                contacts1 = contacts[:]
                for i in contacts1:
                    if len(date) == 5:
                        if i[5][:5] != date:
                            contacts.remove(i)
                    else:
                        if i[5] != date:
                            contacts.remove(i)
                break
            else:
                break
        if not contacts:
            print("Contacts were not found")
            print("Press any key to continue")
            sys.stdin.read(1)
            os.system('cls' if os.name == 'nt' else 'clear')
            continue
        else:
            os.system('cls' if os.name == 'nt' else 'clear')
            print("These contacts were found")
            book.print_contacts(contacts)
            print("Press any key to continue")
            sys.stdin.read(1)
            os.system('cls' if os.name == 'nt' else 'clear')
            continue

    elif command == '5':
        os.system('cls' if os.name == 'nt' else 'clear')
        while True:
            print(
                "Enter name and surname of the contact that you want to delete, type \"all\" so see all contacts or \"back\" to go back to menu: ")
            com = input()
            if com == "all":
                os.system('cls' if os.name == 'nt' else 'clear')
                print(book)
                continue
            elif com == "back":
                break
            else:
                contact = com.split(' ')
                if len(contact) != 2:
                    os.system('cls' if os.name == 'nt' else 'clear')
                    print("Wrong input. Try again")
                    continue
                if not book.get_contacts(contact[0], contact[1]):
                    os.system('cls' if os.name == 'nt' else 'clear')
                    print("Contact was not found. Try again")
                    continue
                os.system('cls' if os.name == 'nt' else 'clear')
                book.print_contacts(book.get_contacts(contact[0], contact[1]))
                print("This contact will be deleted. Are you sure? (1) for YES, (2) for NO: ")
                while True:
                    com = input()
                    ret = False
                    if com == '2':
                        ret = True
                        break
                    elif com == '1':
                        ret = False
                        break
                    else:
                        print("Wrong input. Try again")
                        continue
                if ret:
                    os.system('cls' if os.name == 'nt' else 'clear')
                    continue
                book.delete_contact(contact[0], contact[1])
                os.system('cls' if os.name == 'nt' else 'clear')
                print('{} {} was successfully deleted'.format(contact[0], contact[1]))
                continue

    elif command == '6':
        os.system('cls' if os.name == 'nt' else 'clear')
        while True:
            print(
                "Enter number or list of numbers comma separated of the contacts you want to delete,\ntype \"all\" so see all contacts or \"back\" to go back to menu: ")
            com = input()
            if com == "all":
                os.system('cls' if os.name == 'nt' else 'clear')
                print(book)
                continue
            elif com == "back":
                break
            else:
                nums = [i.strip() for i in com.split(',')]
                f = False
                for i in nums:
                    if not PhoneBook.check_number(i):
                        os.system('cls' if os.name == 'nt' else 'clear')
                        print("Wrong input. Try again")
                        f = True
                        break
                if f:
                    continue
                for i in nums:
                    if i[0] == '+':
                        i = '8' + i[2:]
                contacts = book.get_contacts()
                cont1 = []
                for i in contacts:
                    for j in nums:
                        if i[2].find(j) != -1 or i[3].find(j) != -1 or i[4].find(j) != -1:
                            cont1.append(i)
                            break
                contacts = cont1
                if not contacts:
                    os.system('cls' if os.name == 'nt' else 'clear')
                    print("No contacts found. Try again")
                    continue
                os.system('cls' if os.name == 'nt' else 'clear')
                book.print_contacts(contacts)
                if len(contacts) == 1:
                    print("Delete this contact? \"Y\" for yes or \"N\" to go back")
                    while True:
                        com = input()
                        if com == 'Y':
                            book.delete_contact(contacts[0][0], contacts[0][1])
                            os.system('cls' if os.name == 'nt' else 'clear')
                            print("Contact successfully deleted")
                            break
                        elif com == 'N':
                            os.system('cls' if os.name == 'nt' else 'clear')
                            print("Deletion cancelled")
                            break
                        else:
                            print("wrong input. Try again")
                else:
                    print(
                        "These contacts were found. Enter number or numbers of contacts you want to delete comma separated (1-{})\nor print \"skip\"".format(
                            len(contacts)))
                    while True:
                        com = input()
                        if com == 'skip':
                            os.system('cls' if os.name == 'nt' else 'clear')
                            print("Deletion cancelled")
                            break
                        nums = [i.strip() for i in com.split(',')]
                        f = True
                        for i in nums:
                            for j in range(1, len(contacts) + 1):
                                if i == str(j):
                                    break
                            else:
                                f = False
                                break
                        if not f:
                            print("Wrong input. Try again")
                            continue
                        nums = [int(i) - 1 for i in set(nums)]
                        for i in nums:
                            book.delete_contact(contacts[i][0], contacts[i][1])
                        os.system('cls' if os.name == 'nt' else 'clear')
                        print("Contacts successfully deleted")
                        break


    elif command == '7':
        while True:
            print(
                "Enter name and surname of the contact, type \"all\" so see all contacts or \"back\" to go back to menu: ")
            com = input()
            if com == "all":
                os.system('cls' if os.name == 'nt' else 'clear')
                print(book)
                continue
            elif com == "back":
                break
            else:
                contact = com.split(' ')
                if len(contact) != 2:
                    os.system('cls' if os.name == 'nt' else 'clear')
                    print("Wrong input. Try again")
                    continue
                if not book.get_contacts(contact[0], contact[1]):
                    os.system('cls' if os.name == 'nt' else 'clear')
                    print("Contact was not found. Try again")
                    continue
                if book.get_contacts(contact[0], contact[1])[0][5] == '':
                    os.system('cls' if os.name == 'nt' else 'clear')
                    print("This contact has no date of birth. Try again")
                    continue
                os.system('cls' if os.name == 'nt' else 'clear')
                book.print_contacts(book.get_contacts(contact[0], contact[1]))
                age = book.get_age(contact[0], contact[1])
                print("{} {} is {} years old. Press Enter to continue".format(contact[0], contact[1], age))
                input()
                os.system('cls' if os.name == 'nt' else 'clear')
                continue

    elif command == '8':
        os.system('cls' if os.name == 'nt' else 'clear')
        contacts = book.get_nearest_birthdays()
        if not contacts:
            print("There are no contacts with birthday in the next 30 days.\n Press Enter to continue")
            input()
            continue
        for i in contacts:
            print("{} {}`s birthday will be on {}".format(i[0], i[1], i[5][:5]))
        print("Press Enter to continue")
        input()
        continue

    elif command == '9':
        os.system('cls' if os.name == 'nt' else 'clear')
        while True:
            print(
                "Enter \">n\" to see contacts over n years old, \"<n\" under n years old, \"=n\" exactly n years old:")
            com = input()
            if len(com) < 2:
                os.system('cls' if os.name == 'nt' else 'clear')
                print("Wrong input. Try again")
                continue
            mode = com[0]
            age = com[1:]
            if not (mode == '<' or mode == '>' or mode == '='):
                os.system('cls' if os.name == 'nt' else 'clear')
                print("Wrong input. Try again")
                continue
            f = False
            for i in age:
                if not ('0' <= i <= '9'):
                    f = True
                    break
            if f:
                os.system('cls' if os.name == 'nt' else 'clear')
                print("Wrong input. Try again")
                continue
            contacts = book.get_sorted_contacts(mode, int(age))
            if not contacts:
                print("No contacts found. Press enter to continue")
                input()
                break
            print("Age of these contacts {} {}".format(mode, int(age)))
            book.print_contacts(contacts)
            print("Press enter to continue")
            input()
            break

    else:
        print("Wrong input. Try again")
        skip = True
