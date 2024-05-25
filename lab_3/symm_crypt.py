import os
import logging

from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

from SuppFunc import HelpFunc


class SymmCrypt:
    """
    Symmetric Cryptography class for encryption and decryption.

    Attributes:
        key_len (int): The length of the symmetric key in bits.

    Methods:
        __init__(self, key_len: int = 128): Initializes the SymmCrypt object with the specified key length.
        generate_key(): Generates a symmetric key of specified length.
        encrypt_text(sym_key, encrypted_text_path, iv_path, text): Encrypts the given text using the symmetric key and saves the encrypted text to a file.
        decrypt_text(sym_key, decrypted_text_path, iv_path, ciphertext_path): Decrypts the given ciphertext using the symmetric key and saves the decrypted text to a file.
    """

    def __init__(self, key_len: int = 128) -> None:
        """
        Initializes the SymmCrypt object with the specified key length.

        Args:
            key_len (int): The length of the symmetric key in bits. Default is 128.
        """
        self.key_len = key_len


    def generate_key(self) -> bytes:
        """
        Generates a symmetric key of the specified length.

        Returns:
            bytes: The generated symmetric key.
        """
        try:
            return os.urandom(self.key_len // 8)
        except Exception as e:
            logging.error(f"Failed to generate key: {e}")
            raise


    def encrypt_text(self, sym_key: bytes, encrypted_text_path: str, iv_path: str, text: bytes) -> None:
        """
        Encrypts the given text using the symmetric key and saves the encrypted text to a file.

        Args:
            sym_key (bytes): The symmetric key used for encryption.
            encrypted_text_path (str): The path where the encrypted text will be saved.
            iv_path (str): Path to the iv text file
            text (bytes): The text to be encrypted.
        """
        try:
            iv = os.urandom(16)
            cipher = Cipher(algorithms.SEED(sym_key), modes.CBC(iv))
            encryptor = cipher.encryptor()
            padder = padding.PKCS7(128).padder()
            padded_text = padder.update(text) + padder.finalize()
            ciphertext = encryptor.update(padded_text) + encryptor.finalize()
            with open(iv_path, "wb") as iv_file:
                iv_file.write(iv)
            with open(encrypted_text_path, "wb") as encrypted_text_file:
                encrypted_text_file.write(ciphertext)
        except Exception as e:
            logging.error(f"Failed to encrypt text: {e}")
            raise


    def decrypt_text(self, sym_key: bytes, decrypted_text_path: str, iv_path:str, ciphertext_path: str) -> None:
        """
        Decrypts the given ciphertext using the symmetric key and saves the decrypted text to a file.

        Args:
            sym_key (bytes): The symmetric key used for decryption.
            iv_path (str) : Path to the iv text file
            decrypted_text_path (str): The path where the decrypted text will be saved.
            ciphertext_path (str): The ciphertext to be decrypted.
        """
        try:
            iv = HelpFunc.read_file(iv_path)
            ciphertext = HelpFunc.read_file(ciphertext_path)
            cipher = Cipher(algorithms.SEED(sym_key), modes.CBC(iv))
            decryptor = cipher.decryptor()
            plaintext = decryptor.update(ciphertext) + decryptor.finalize()
            unpadder = padding.PKCS7(128).unpadder()
            plaintext = unpadder.update(plaintext) + unpadder.finalize()
            with open(decrypted_text_path, "wb") as decrypted_text_file:
                decrypted_text_file.write(plaintext)
        except Exception as e:
            logging.error(f"Failed to decrypt text: {e}")
            raise