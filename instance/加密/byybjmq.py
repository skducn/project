# -*- coding: utf-8 -*-
# *****************************************************************
# Author     : John
# Date       : 2023-4-17
# Description: # 北约音标加密器
# http://www.51testing.com/html/13/n-7795813.html
# *****************************************************************
def encrypt_message(message):
    nato_alphabet = {'A': 'Alfa', 'B': 'Bravo', 'C': 'Charlie', 'D': 'Delta',
    'E': 'Echo', 'F': 'Foxtrot', 'G': 'Golf', 'H': 'Hotel',
    'I': 'India', 'J': 'Juliet', 'K': 'Kilo', 'L': 'Lima',
    'M': 'Mike', 'N': 'November', 'O': 'Oscar', 'P': 'Papa',
    'Q': 'Quebec', 'R': 'Romeo', 'S': 'Sierra', 'T': 'Tango',
    'U': 'Uniform', 'V': 'Victor', 'W': 'Whiskey', 'X': 'Xray',
    'Y': 'Yankee', 'Z': 'Zulu'}

    encrypted_message = ''
    for letter in message:
        if letter.upper() in nato_alphabet:
            encrypted_message += nato_alphabet[letter.upper()] + ''
        else:
            encrypted_message += letter
    return encrypted_message
message = "Hello World"
encrypted_message = encrypt_message(message)
print("Encrypted message: ", encrypted_message)













