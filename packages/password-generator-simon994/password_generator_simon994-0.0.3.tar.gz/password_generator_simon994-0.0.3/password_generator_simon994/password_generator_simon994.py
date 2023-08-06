import string, random

def generate_password(default_length=10):
    inputted_length = input("How long should the password be? Please provide a number or hit enter for default length of 10: ")
    password_length = 10 if len(inputted_length) == 0 else int(inputted_length)
    available_characters = string.ascii_letters + string.digits + string.punctuation
    password = ''
    for i in range(password_length):
        password += (random.choice(available_characters))

    print(password)



