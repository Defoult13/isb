import json
import os

from enum import Enum, auto
from typing import Tuple, Dict


class CipherMode(Enum):
    ENCRYPT = 1
    DECRYPT = 2


def caesar_cipher(text: str, shift: int, mode: CipherMode) -> Tuple[str, Dict[str, str]]:
    """
    Encrypts or decrypts the text using the Caesar cipher with the specified shift.

    Args:
        text (str): The text to be encrypted or decrypted.
        shift (int): The shift value for encryption or decryption.
        mode (CipherMode): The mode of operation, either encryption or decryption.

    Returns:
        tuple: A tuple containing the encrypted or decrypted text and the key dictionary.
    """
    result = ''
    key = {}
    for char in text:
        if char.isalpha():
            shifted = ord(char) + shift if mode == CipherMode.ENCRYPT else ord(char) - shift

            case_lower = char.islower()
            case_upper = char.isupper()
            case = auto
            match case:
                case True if case_lower:
                    match mode:
                        case CipherMode.ENCRYPT:
                            shifted -= 32 if shifted > ord('я') else 0
                            shifted += 32 if shifted < ord('а') else 0
                        case CipherMode.DECRYPT:
                            shifted += 32 if shifted < ord('а') else 0
                            shifted -= 32 if shifted > ord('я') else 0
                case True if case_upper:
                    match mode:
                        case CipherMode.ENCRYPT:
                            shifted -= 32 if shifted > ord('Я') else 0
                            shifted += 32 if shifted < ord('А') else 0
                        case CipherMode.DECRYPT:
                            shifted += 32 if shifted < ord('А') else 0
                            shifted -= 32 if shifted > ord('Я') else 0

            result += chr(shifted)
            key[char] = chr(shifted)
        else:
            result += char
            key[char] = char

    return result, key


def encoder(input_file: str, output_file: str, shift: int, key_file: str, mode: CipherMode) -> None:
    """
    Encrypts or decrypts the text from the input file and saves the result to the output file.
    Saves the key in JSON format.

    Args:
        input_file (str): The path to the input file containing the text.
        output_file (str): The path to the file where the result will be saved.
        shift (int): The shift value for encryption or decryption.
        key_file (str): The path to the file where the key will be saved.
        mode (CipherMode): The mode of operation. Can be CipherMode.ENCRYPT or CipherMode.DECRYPT.
    """
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            text = f.read()
        match mode:
            case CipherMode.ENCRYPT:
                encoded_text, key = caesar_cipher(text, shift, CipherMode.ENCRYPT)
            case CipherMode.DECRYPT:
                encoded_text, key = caesar_cipher(text, shift, CipherMode.DECRYPT)

        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(encoded_text)

        with open(key_file, 'w', encoding='utf-8') as f:
            json.dump(key, f, ensure_ascii=False, indent=4)

    except FileNotFoundError:
        print("File not found. Please check the file path.")
    except Exception as e:
        print("An error occurred:", e)


if __name__ == '__main__':
    try:
        with open(os.path.join("lab_1", "task1", "config1.json"), 'r', encoding='utf-8') as json_file:
            config = json.load(json_file)


        encoder(config["text_file"], config["crypted_file"], config["shift"], config["Key1"], CipherMode.ENCRYPT)
        encoder(config["crypted_file"], config["decrypted_file"], config["shift"], config["Key3"], CipherMode.DECRYPT)

    except FileNotFoundError:
        print("Config file not found. Please ensure the config file exists in the specified path.")
    except json.JSONDecodeError:
        print("Config file is not valid JSON.")
    except KeyError as e:
        print(f"Key {e} not found in the config file.")
    except Exception as e:
        print("An error occurred:", e)