import random
import csv
import os.path

from configs import path_to_passwords
from datetime import datetime
from fuzzywuzzy import fuzz

chars = '.-abcdefghijklnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'
digits = '1234567890'


def get_file_name(id_user: str):
    return path_to_passwords + str(id_user) + '.csv'


def generate_password(id_user: str, length: int = 12, service_name: str = '', symbols: str = chars):
    password = ''
    for i in range(length):
        password += random.choice(symbols)
    print('Generated password: ' + password)
    if service_name:
        print('For service: ' + service_name)
    save_pass_to_csv(service_name, password, id_user=id_user)
    return password


def check_password(service_name: str, id_user: str):
    filename = get_file_name(id_user)
    if not os.path.exists(filename):
        with open(filename, 'w', newline='') as csv_file:
            print('Creating new password dictionary...')
            writer = csv.writer(csv_file, delimiter=',')
            writer.writerow(['ID', 'ServiceName', 'Password', 'CreatedTime'])
    else:
        # check if there is no any passwords for services
        passwords = read_all_passwords(id_user)
        for record in passwords:
            serching_ratio = fuzz.WRatio(record[1], service_name)
            if serching_ratio > 65:
                print("Error! Password for this service already exists")
                return False

    return True


def save_pass_to_csv(service_name: str, password: str, id_user: str):
    filename = get_file_name(id_user)
    passwords = read_all_passwords(id_user)
    index = 0
    if len(passwords) > 0:
        index = int(passwords[-1][0]) + 1
    with open(filename, 'a', newline='') as csv_file:
        print(f'Appending password "{password}" to dictionary...')
        writer = csv.writer(csv_file, delimiter=',')
        if len(service_name) == 0:
            service_name = str(index)

        writer.writerow([index, service_name, password, str(datetime.now().timestamp())])


def get_passwords(id_user: str):
    passwords = read_all_passwords(id_user)
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


def read_all_passwords(id_user: str, take_titles: bool = False):
    filename = get_file_name(id_user)
    if os.path.exists(filename):
        with open(filename, 'r') as csv_file:
            pass_dictionary = list()
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


def find_password_by_service_name(service_name: str, id_user: str):
    print('Trying to find password for service ' + service_name)
    passwords = read_all_passwords(id_user)
    rec = list()
    for record in passwords:
        searching_ratio = fuzz.WRatio(record[1], service_name)
        if searching_ratio > 65:
            rec.append(record)

    if len(rec) == 1:
        print(f'Password for service {service_name} was founded')
    return rec


def find_service_by_id(password_id: str, id_user: str):
    print('Trying to find password for id ' + password_id)
    passwords = read_all_passwords(id_user)
    for record in passwords:
        if record[0] == password_id:
            return record


def rewrite_passwords_dictionary(passwords, id_user: str):
    filename = get_file_name(id_user)
    with open (filename, 'w', newline='') as csv_file:
        writer = csv.writer(csv_file, delimiter=',')
        writer.writerows(passwords)


def update_password_by_id(pass_id: str, new_password: str, id_user: str):
    # todo: refactor this shitty part
    passwords = read_all_passwords(take_titles=True, id_user=id_user)

    password = find_service_by_id(pass_id, id_user=id_user)
    password[2] = new_password

    i = 0
    for recs in passwords:
        if recs[0] == password[0]:
            passwords[i] = password
            break
        i += 1

    rewrite_passwords_dictionary(passwords, id_user=id_user)
    print('Updated password')


def delete_password_by_id(pass_id: str, id_user: str):
    passwords = read_all_passwords(take_titles=True, id_user=id_user)

    passwords.remove(find_service_by_id(pass_id, id_user=id_user))

    rewrite_passwords_dictionary(passwords, id_user=id_user)

    print('Deleted with success')









