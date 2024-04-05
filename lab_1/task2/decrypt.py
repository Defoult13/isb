import json
import os


def decrypt_text(text_file, dictionary_file, output_file) -> None:

    """
    Decrypts text from the specified file using the dictionary from the specified JSON file
    and saves the result in a new file.

    Args:
    text_file (str): Name of the file containing the encrypted text.
    dictionary_file (str): Name of the JSON file containing the dictionary for decryption.
    output_file (str): Name of the file to which the decrypted text will be saved.

    Returns:
    None
    """

    try:
        current_dir = os.getcwd()
        text_file_path = os.path.join(current_dir, text_file)
        dictionary_file_path = os.path.join(current_dir, dictionary_file)
        output_file_path = os.path.join(current_dir, output_file)

        with open(dictionary_file_path, 'r', encoding='utf-8') as json_file:
            dictionary = json.load(json_file)

        decrypted_text = ""

        with open(text_file_path, 'r', encoding='utf-8') as file:
            file_text = file.read()
            for char in file_text:
                decrypted_char = dictionary.get(char, char)
                decrypted_text += decrypted_char

        with open(output_file_path, 'w', encoding='utf-8') as output:
            output.write(decrypted_text)

        print("Дешифрованный текст сохранен в файле:", output_file_path)

    except FileNotFoundError:
        print("File not found. Please check the file paths.")
    except Exception as e:
        print("An error occurred:", e)


if __name__ == '__main__':
    try:
        with open(os.path.join("lab_1","task2","config.json"), 'r', encoding='utf-8') as json_file:
            config = json.load(json_file)
        decrypt_text(config["text_file"], config["dictionary_file"], config["output_file"])

    except FileNotFoundError:
        print("Config file not found. Please ensure the config file exists in the specified path.")
    except json.JSONDecodeError:
        print("Config file is not valid JSON.")
    except KeyError as e:
        print(f"Key {e} not found in the config file.")
    except Exception as e:
        print("An error occurred:", e)
