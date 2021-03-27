import random
import csv
import os.path

from datetime import datetime

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
            writer.writerow(['ID', 'ServiceName', 'Password', 'CreatedTime'])
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

        writer.writerow([index, service_name, password, str(datetime.now().timestamp())])


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


def read_all_passwords(filename: str = 'passwords_book.csv', take_titles: bool = False) -> list[str, str, str, str]:
    if os.path.exists(filename):
        with open(filename, 'r') as csv_file:
            pass_dictionary = list[str, str, str, str]()
            reader = csv.reader(csv_file)
            i = 0
            for row in reader:
                if take_titles:
                    pass_dictionary.append([row[0], row[1], row[2], row[3]])
                elif i > 0:
                    pass_dictionary.append([row[0], row[1], row[2], row[3]])
                i += 1
            return pass_dictionary
    return []


def find_password_by_service_name(service_name: str):
    print('Trying to find password for service ' + service_name)
    passwords = read_all_passwords()
    rec = list[str, str, str, str]()
    for record in passwords:
        if service_name == record[1]:
            rec = record
            break
    print(f'Password for service {service_name} was founded')
    return rec


def rewrite_passwords_dictionary(passwords, filename: str = 'passwords_book.csv' ):
    with open (filename, 'w', newline='') as csv_file:
        writer = csv.writer(csv_file, delimiter=',')
        writer.writerows(passwords)


def update_password_by_service(service_name: str, new_password: str):
    # todo: refactor this shitty part
    passwords = read_all_passwords(take_titles=True)

    password = find_password_by_service_name(service_name)
    password[2] = new_password

    i = 0
    for recs in passwords:
        if recs[0] == password[0]:
            passwords[i] = password
            break
        i += 1

    rewrite_passwords_dictionary(passwords)
    print('Updated password')


def delete_password_by_service(service_name: str):
    passwords = read_all_passwords(take_titles=True)

    passwords.remove(find_password_by_service_name(service_name))

    rewrite_passwords_dictionary(passwords)

    print('Deleted with success')






