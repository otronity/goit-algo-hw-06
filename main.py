import re
from collections import UserDict

class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

class Name(Field):
    def __init__(self, name):
        self.value = name

class Phone(Field):
    def __init__(self, phone):
        super().__init__(phone)  
        if bool(re.match(r'^\d{10}$', phone)):
            self.value = phone
        else:
            raise ValueError('Incorrect Phone number')

    # Изменяем номер телефона с проверкой на корректность нового номера   
    def change_phone(self, phone):
        if bool(re.match(r'^\d{10}$', phone)):
            self.value = phone
        else:
            raise ValueError('Incorrect New Phone number')
        
class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []

    def add_phone(self, phone):
        if not any(p.value == phone for p in self.phones):
            self.phones.append(Phone(phone))

    def edit_phone(self, phoneold, phonenew):
        # перевіряємо чи є номер який хочемо зінити в перліку телефонів
        if not any(p.value == phoneold for p in self.phones):
            raise ValueError(f'Incorrect Phone number {phoneold}')
        for phone in self.phones:
            if phone.value == phoneold:
                # перевіряємо чи є новий номер вже в перліку телефонів
                if not any(p.value == phonenew for p in self.phones):
                    phone.change_phone(phonenew)
                else:
                    self.remove_phone(phoneold)
                break

    def find_phone(self, phone):
        result = list(filter(lambda record: record.value == phone, self.phones))
        return result[0] if len(result) > 0 else None
    
    def remove_phone(self, phone):
        phonedel = self.find_phone(phone)
        if phonedel:
            self.phones.remove(phonedel)

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"

class AddressBook(UserDict):
    def add_record(self, record):        
        self.data[record.name.value] = record

    def find(self, name):
        result = list(filter(lambda record: record.name.value == name, self.data.values()))
        return result[0] if len(result) > 0 else None
    
    def delete(self, name):
        del self.data[name]

    def __str__(self):
        if not self.data:
            return "Address Book is empty."

        contacts_str = "\n".join([f"{record.name.value}: {', '.join(p.value for p in record.phones) if record.phones else 'No phones'}"
                                 for record in self.data.values()])
        return f"Address Book:\n{contacts_str}"
        
if __name__ == "__main__":
# Створення нової адресної книги
    book = AddressBook()

    # Створення запису для John
    john_record = Record("John")
    john_record.add_phone("1234567890")
    john_record.add_phone("5555555555")

    # Додавання запису John до адресної книги
    book.add_record(john_record)

    # Створення та додавання нового запису для Jane
    jane_record = Record("Jane")
    jane_record.add_phone("9876543210")
    book.add_record(jane_record)

    # Виведення всіх записів у книзі
     
    print(book)

    # Знаходження та редагування телефону для John
    john = book.find("John")
    john.edit_phone("1234567890", "1112223333")

    print(john)  # Виведення: Contact name: John, phones: 1112223333; 5555555555

    # Пошук конкретного телефону у записі John
    found_phone = john.find_phone("5555555555")
    print(f"{john.name}: {found_phone}")  # Виведення: John: 5555555555

    # Видалення запису Jane
    book.delete("Jane")
