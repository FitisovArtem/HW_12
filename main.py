from collections import UserDict
from datetime import datetime
import json
import os

FILENAME = "AddressBook.json"


class Field:
    def __init__(self, value):
        self.__value = None
        self.value = value


class Name:
    def __init__(self, name):
        self.value = name


class Phone(Field):
    def __init__(self, phone):
        self.__value = None
        self.value = phone

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, phone):
        if not self.is_validate_phone(phone):
            raise AttributeError("Number is not Valid!")

    def is_validate_phone(self, phone_for_validation):
        new_phone = (
            phone_for_validation.strip()
            .replace("+", "")
            .replace("(", "")
            .replace(")", "")
            .replace("-", "")
            .replace(" ", "")
        )
        if new_phone.isdigit():
            self.__value = new_phone
            return True
        return False


class Birthday(Field):
    def __init__(self, birthday):
        self.__birthday = None
        self.birthday = birthday

    @property
    def birthday(self):
        return self.__birthday

    @birthday.setter
    def birthday(self, birthday):
        try:
            datetime.strptime(birthday, '%d.%m.%Y')
        except ValueError:
            raise 'Invalid date! Date format should be: dd.mm.YYYY'
        self.__birthday = birthday


class Record:
    def __init__(self, name, phones, birthday=None):
        self.name = name
        self.phones = [phones]
        self.birthday = birthday

    def add(self):
        pass

    def delete(self):
        pass

    def change(self):
        pass

    def days_to_birthday(self):
        print(self, self.birthday)
        if self.birthday is None:
            return "Дата рождения не задана"

        b_now = datetime.now()

        print(self.birthday)
        b_d = datetime(b_now.year, self.birthday.birthday.month, self.birthday.birthday.day + 1)

        diff = b_d - b_now

        if diff.days < 0:
            bd_new = datetime(b_now.year + 1, self.birthday.birthday.month, self.birthday.birthday.day)
            difference = bd_new - b_now
            return difference.days
        return


class AddressBook(UserDict):
    def add_record(self, record: Record):
        self.data[record.name.value] = record

        if os.path.exists(FILENAME):
            with open(FILENAME, "r", encoding="utf-8") as fh:
                ad_book_list = json.load(fh)
            for el in ad_book_list:
                if el.get('name') == record.name.value:
                    ad_book_list.remove(el)
                    break
        else:
            ad_book_list = []

        contact = {"name": record.name.value, "phones": [ph.value for ph in record.phones],
                   "birthday": record.birthday.birthday}
        ad_book_list.append(contact)
        with open(FILENAME, "w", encoding="utf-8") as file:
            json.dump(ad_book_list, file, indent=4, ensure_ascii=False)

    def find_record(self, value):
        with open(FILENAME, "r", encoding="utf-8") as fh:
            book_list = json.load(fh)
        result = []
        for el in book_list:
            for n, v in el.items():
                if value in str(v):
                    result.append(el)
        if len(result) > 0:
            return result
        else:
            return f"По данным: {value} не найдено совпадений в книге контактов"

    def iterator(self, count_data) -> None:
        myIterAddressBookList = IterAddressBook(count_data)
        for ran in myIterAddressBookList:
            print(ran, end=' ')


class IterAddressBook:
    def __init__(self, count_data):
        self.iter = -1
        self.count_data = count_data

    def __iter__(self):
        return self

    def __next__(self):
        self.iter += 1
        if self.iter < self.count_data:
            return ab.data[list(ab.data.keys())[self.iter]]
        else:
            raise StopIteration


if __name__ == "__main__":
    name1 = Name('Bill')
    phone1 = Phone('+   (   ) 1234567890')
    bd1 = Birthday('01.01.1999')
    rec1 = Record(name1, phone1, bd1)
    ab = AddressBook()
    ab.add_record(rec1)

    name2 = Name('Mary')
    phone2 = Phone('+   (   ) 453534534534')
    bd2 = Birthday('01.01.1970')
    rec2 = Record(name2, phone2, bd2)
    ab.add_record(rec2)

    assert isinstance(ab['Bill'], Record)
    assert isinstance(ab['Bill'].name, Name)
    assert isinstance(ab['Bill'].birthday, Birthday)
    assert isinstance(ab['Bill'].phones, list)
    assert isinstance(ab['Bill'].phones[0], Phone)
    assert ab['Bill'].phones[0].value == '1234567890'

    print(ab.find_record("789"))

    print('All Ok)')
