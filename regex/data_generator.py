import random
import string


def generate_random_plate():
    plate = 'H'
    plate += ''.join(random.choice(string.ascii_uppercase) for _ in range(2))
    plate += ''.join(str(random.randint(0, 9)) for _ in range(random.randint(3, 4)))
    return plate


def generate_hannover_license_plates_to_file(num_entries, filename):
    data = []
    for _ in range(num_entries):
        if random.randint(0, 1) == 0:
            data.append('BS' + generate_random_plate())
        else:
            data.append('WOB' + generate_random_plate())
        data.append(generate_random_plate())

    random.shuffle(data)

    with open(filename, 'w') as file:
        for plate in data:
            file.write(plate + '\n')


def generate_phone_numbers_to_file(num_entries, filename):
    data = []
    for _ in range(num_entries):
        country_code = '+' + str(random.randint(1, 999))
        area_code = '(' + str(random.randint(100, 9999)) + ')' if random.randint(0, 1) == 0 else ''
        main_number = ''.join(random.choice('0123456789- ') for _ in range(random.randint(7, 10)))
        phone_number = country_code + ' ' + area_code + ' ' + main_number
        data.append(phone_number)

    with open(filename, 'w') as file:
        for phone in data:
            file.write(phone + '\n')


def main():
    generate_hannover_license_plates_to_file(200, "license_plates.txt")
    generate_phone_numbers_to_file(200, "phone_numbers.txt")


if __name__ == "__main__":
    main()
