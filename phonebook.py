from prettytable import PrettyTable
import sqlite3


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


    def get_contacts(self, name=None, surname=None):
        if name is None and surname:
            s = "SELECT * FROM phonebook WHERE surname=?"
            self.cursor.execute(s, [surname])
        elif surname is None and name:
            s = "SELECT * FROM phonebook WHERE name=?"
            self.cursor.execute(s, [name])
        elif name and surname:
            s = "SELECT * FROM phonebook WHERE name=? AND surname=?"
            self.cursor.execute(s, [name, surname])
        else:
            s = "SELECT * FROM phonebook"
            self.cursor.execute(s)
        return self.cursor.fetchall()

    def create_contact(self, name, surname):
        if self.get_contacts(name, surname):
            return False
        self.cursor.execute("INSERT INTO phonebook VALUES (?, ?, '', '', '', '')", [name, surname])
        self.conn.commit()
        return True

    def edit_contact(self, name, surname, newname=None, newsurname=None):
        if newsurname is None:
            self.cursor.execute("UPDATE phonebook SET name = ? WHERE name=? AND surname=?", [newname, name, surname])
            self.conn.commit()
        elif newname is None:
            self.cursor.execute("UPDATE phonebook SET surname = ? WHERE name=? AND surname=?", [newsurname, name, surname])
            self.conn.commit()
        else:
            self.cursor.execute("UPDATE phonebook SET name = ?, surname = ? WHERE name=? AND surname=?", [newname, newsurname, name, surname])
            self.conn.commit()

    def delete_contact(self, name, surname):
    	self.cursor.execute("DELETE FROM phonebook WHERE name = ? AND surname = ?", [name, surname])
    	self.conn.commit()
    	return


    def add_number(self, name, surname, category, number):
        self.cursor.execute("SELECT {} FROM phonebook WHERE name=? AND surname=?".format(category), [name, surname])
        nums = self.cursor.fetchone()[0]
        nums = nums + ', {}'.format(number) if nums else number
        self.cursor.execute("UPDATE phonebook SET {}='{}' WHERE name=? AND surname=?".format(category, nums), [name, surname])
        self.conn.commit()

    def add_numbers(self, name, surname, category, numbers):
        nums = ', '.join(numbers)
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


    def print_contacts(self, data):
        x = PrettyTable()
        x.field_names = ['name', 'surname', 'mobile', 'working', 'home', 'date']
        x.add_rows(data)
        print(x)
        return


    @staticmethod
    def check_number(number):
        return True

    @staticmethod
    def check_date(date):
        return True

    @staticmethod
    def check_name(name):
        return True