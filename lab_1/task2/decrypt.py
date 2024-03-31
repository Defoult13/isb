import json
import os


def decrypt_text(text_file, dictionary_file, output_file):

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

    
    current_dir = os.getcwd()
    text_file_path = os.path.join(current_dir, text_file)
    dictionary_file_path = os.path.join(current_dir, dictionary_file)
    output_file_path = os.path.join(current_dir, output_file)

    with open(dictionary_file_path, 'r', encoding='utf-8') as json_file:
        dictionary = json.load(json_file)

    decrypted_text = ""

    with open(text_file_path, 'r', encoding='utf-8') as file:
        for line in file:
            for char in line:
                decrypted_char = dictionary.get(char, char)
                decrypted_text += decrypted_char

    
    with open(output_file_path, 'w', encoding='utf-8') as output:
        output.write(decrypted_text)

    print("Дешифрованный текст сохранен в файле:", output_file_path)


if __name__ == '__main__':
    with open(os.path.join("lab_1","task2","config.json"), 'r', encoding='utf-8') as json_file:
        config = json.load(json_file)
    decrypt_text(config["text_file"], config["dictionary_file"], config["output_file"])
