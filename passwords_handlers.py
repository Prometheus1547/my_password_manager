import random
import csv
import os.path

chars = '.-abcdefghijklnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'


def generate_password(length: int = 12, name: str = ''):
    password = ''
    for i in range(length):
        password += random.choice(chars)
    print('Generated password: ' + password)
    if name:
        print('For service: ' + name)
    save_pass_to_csv(name, password)
    return password


def save_pass_to_csv(service_name: str, password: str, filename: str = 'passwords_book.csv'):
    if not os.path.exists(filename):
        with open(filename, 'w', newline='') as csv_file:
            writer = csv.writer(csv_file, delimiter=',')
            writer.writerow(['ServiceName', 'Password'])
    with open(filename, 'a', newline='') as csv_file:
        writer = csv.writer(csv_file, delimiter=',')
        writer.writerow([service_name, password])


def get_passwords():
    passwords = read_all_passwords()
    pass_lines = []
    if len(passwords) == 0:
        return ''
    for row in passwords:
        password = row[1]
        service_name = ''
        if len(row[0]) == 0:
            service_name = 'blank'
        else:
            service_name = row[0]
        pass_lines.append(service_name + ':' + password)

    print(pass_lines)
    return '\n'.join(pass_lines, )


def read_all_passwords(filename: str = 'passwords_book.csv'):
    if os.path.exists(filename):
        with open(filename, 'r') as csv_file:
            pass_dictionary = []
            reader = csv.reader(csv_file)
            i = 0
            for row in reader:
                if i > 0:
                    pass_dictionary.append([row[0], row[1]])
                i += 1
            return pass_dictionary
    return []



