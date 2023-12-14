import random
import string

def generate_random_phone_numbers(num_entries):
    phone_numbers = []

    for _ in range(num_entries):
        # Generate a random phone number pattern
        country_code = random.choice(["+1", "001", "+44", "+49", "+33", "+61", "+81", "+91"])
        separator = random.choice([" ", "-", ".", "(", ""])
        number = ''.join(random.choices(string.digits, k=10))

        # Create the phone number entry
        phone_number = f"{country_code}{separator}{number}"
        phone_numbers.append(phone_number)

    return phone_numbers

# Generate 1000 random phone number entries
phone_numbers = generate_random_phone_numbers(1000)

# Save the phone numbers to a text file
with open("phone_numbers.txt", "w") as file:
    for entry in phone_numbers:
        file.write(entry + "\n")

print("Random phone numbers generated and saved to phone_numbers.txt.")
