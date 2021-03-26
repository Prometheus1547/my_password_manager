import random
import csv
import os.path

chars = '.-abcdefghijklnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'


def generate_password(length: int = 12, service_name: str = ''):
    password = ''
    for i in range(length):
        password += random.choice(chars)
    print('Generated password: ' + password)
    if service_name:
        print('For service: ' + service_name)
    save_pass_to_csv(service_name, password)
    return password


def check_password(service_name: str, filename: str = 'passwords_book.csv'):
    if not os.path.exists(filename):
        with open(filename, 'w', newline='') as csv_file:
            print('Creating new password dictionary...')
            writer = csv.writer(csv_file, delimiter=',')
            writer.writerow(['ID', 'ServiceName', 'Password'])
    else:
        # check if there is no any passwords for services
        passwords = read_all_passwords()

        if service_name in [item[1] for item in passwords]:
            print("Error! Password for this service already exists")
            return False

    return True


def save_pass_to_csv(service_name: str, password: str, filename: str = 'passwords_book.csv'):
    passwords = read_all_passwords()
    index = 0
    if len(passwords) > 0:
        index = int(passwords[-1][0]) + 1
    with open(filename, 'a', newline='') as csv_file:
        print(f'Appending password "{password}" to dictionary...')
        writer = csv.writer(csv_file, delimiter=',')
        if len(service_name) == 0:
            service_name = str(index)
        writer.writerow([index, service_name, password])


def get_passwords():
    passwords = read_all_passwords()
    pass_lines = []
    if len(passwords) == 0:
        return ''
    for row in passwords:
        password = row[2]
        service_name = ''
        if len(row[1]) == 0:
            service_name = 'blank'
        else:
            service_name = row[1]
        pass_lines.append(service_name + ':' + password)

    print(pass_lines)
    return pass_lines


def read_all_passwords(filename: str = 'passwords_book.csv') -> list[str, str, str]:
    if os.path.exists(filename):
        with open(filename, 'r') as csv_file:
            pass_dictionary = list[str, str]()
            reader = csv.reader(csv_file)
            i = 0
            for row in reader:
                if i > 0:
                    pass_dictionary.append([row[0], row[1], row[2]])
                i += 1
            return pass_dictionary
    return []


def find_password_by_service_name(service_name: str):
    print('Trying to find password for service ' + service_name)
    passwords = read_all_passwords()
    password = ''
    for record in passwords:
        if service_name == record[1]:
            password = record[2]
    print(f'Password for service {service_name} was founded')
    return password





