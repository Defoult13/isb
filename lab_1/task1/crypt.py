import json
import os
from typing import Tuple, Dict

def caesar_cipher(text: str, shift: int) -> Tuple[str, Dict[str, str]]:
    """
    Encrypts the text using the Caesar cipher with the specified shift.

    Args:
        text (str): The original text to be encrypted.
        shift (int): The shift value for encryption.

    Returns:
        tuple: A tuple containing the encrypted text and the key dictionary.
    """
    result = ''
    key = {}
    for char in text:
        if char.isalpha():
            shifted = ord(char) + shift
            if char.islower():
                if shifted > ord('я'):
                    shifted -= 32
                elif shifted < ord('а'):
                    shifted += 32
            elif char.isupper():
                if shifted > ord('Я'):
                    shifted -= 32
                elif shifted < ord('А'):
                    shifted += 32
            result += chr(shifted)
            key[char] = chr(shifted)
        else:
            result += char
            key[char] = char
    return result, key

def encoder(input_file: str, output_file: str, shift: int, key_file: str) -> None:
    """
    Encrypts the text from the input file and saves the result to the output file.
    Saves the key in JSON format.

    Args:
        input_file (str): The path to the input file containing the original text.
        output_file (str): The path to the file where the encrypted text will be saved.
        shift (int): The shift value for encryption.
        key_file (str): The path to the file where the key will be saved.
    """
    with open(input_file, 'r', encoding='utf-8') as f:
        text = f.read()

    encoded_text, key = caesar_cipher(text, shift)

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(encoded_text)

    reversed_key = {v: k for k, v in key.items()}
    with open(key_file, 'w', encoding='utf-8') as f:
        json.dump(reversed_key, f, ensure_ascii=False, indent=4)

if __name__ == '__main__':
    with open(os.path.join("lab_1", "task1", "config1.json"), 'r', encoding='utf-8') as json_file:
        config = json.load(json_file)
    
    encoder(config["text_file"], config["crypted_file"], config["shift"], config["Key1"])