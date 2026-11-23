ENGLISH_ALPHABET = ["ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"]
AL_BHED_ALPHABET = ["YPLTAVKREZGMSHUBXNCDIJFQOWypltavkrezgmshubxncdijfqow"]


def substitute_message(message, source_alphabet, target_alphabet, key):
    result = message
    for _ in range(key):
        translated_message = ""

        for character in result:
            match_found = False

user_input = input("Input here: ")

def encode_func():
    substitute_message(user_input, ENGLISH_ALPHABET, AL_BHED_ALPHABET, 2)
