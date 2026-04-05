#password strenght should be choice(weak,medium,strong)
#weak password should be just word from list or combination of two words
#medium will contain small and capital letters
#strong will contain numbers and symbols on top of letters
#user should be able to choose password lenght and password strenght before generating
import random
import string

def ask_user():
    strenght = input("How strong do you want your password to be ?\n"
                     "w for weak\n"
                     "m for medium\n"
                     "s for strong\n")
    if strenght == 'w':
        print(weak_password())
    elif strenght == 'm':
        print(medium_password())
    elif strenght == 's':
        print(strong_password())
    else:
        print("Please enter a valid choice")

def weak_password():
    pass1 = ['cat','dog','apple','tree','run','bomb','computer','letter','word','craft']
    pass2 = ['blue','black','yellow','red','road','lenght','table','exwife','yugal','words']
    password = random.choice(pass1) + random.choice(pass2)
    return password

def medium_password():
    password_lenght = int(input("How long should your password be ?"))
    letters = string.ascii_letters
    criteria = False
    pwd = ''
    while criteria == False:
        for i in range(password_lenght):
            char = random.choice(letters)
            pwd += char
        if pwd != pwd.lower() and pwd != pwd.upper():
            criteria = True
    return pwd


def strong_password():
    password_lenght = int(input("How long should your password be ?"))
    letters = string.ascii_letters
    numbers = string.digits
    special = string.punctuation
    chars = letters + numbers + special
    criteria = False
    pwd = ''
    while criteria == False:
        oneletter = 0
        onenumber = 0
        onespecial = 0
        for i in range(password_lenght):
            char = random.choice(chars)
            if char in letters:
                oneletter += 1
            if char in numbers:
                onenumber += 1
            if char in special:
                onespecial += 1
            pwd += char
        if oneletter >= 1 and onenumber >= 1 and onespecial >= 1:
            criteria = True
    return pwd


ask_user()


