import os
import logging

from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes



logging.basicConfig(level=logging.INFO)


class AsymmCrypt:
    """
    Provides methods for asymmetric encryption and decryption using RSA algorithm,
    specifically for encrypting and decrypting SEED keys.

    Methods:
        generate_key_pair(): Generates a pair of RSA private and public keys.
        generate_seed_key() -> bytes: Generates a SEED key.
        encrypt_seed_key_with_public_key(public_key: rsa.RSAPublicKey, seed_key: bytes) -> bytes:
            Encrypts a SEED key with the provided RSA public key.
        decrypt_seed_key_with_private_key(private_key: rsa.RSAPrivateKey, ciphertext: bytes) -> bytes:
            Decrypts a ciphertext with the provided RSA private key to retrieve the SEED key.
    """

    def generate_key_pair(self) -> tuple:
        """
        Generates a pair of RSA private and public keys.

        Returns:
            tuple: A tuple containing RSA private key and public key.
        """
        try:
            private_key = rsa.generate_private_key(
                public_exponent=65537,
                key_size=2048
            )
            public_key = private_key.public_key()
            return private_key, public_key
        except Exception as e:
            logging.error(f"Failed to generate key pair: {e}")
            raise


    def generate_seed_key(self) -> bytes:
        """
        Generates a SEED key.

        Returns:
            bytes: The generated SEED key.
        """
        try:
            return os.urandom(16)
        except Exception as e:
            logging.error(f"Failed to generate SEED key: {e}")
            raise


    def encrypt_seed_key_with_public_key(self, public_key: rsa.RSAPublicKey, seed_key: bytes) -> bytes:
        """
        Encrypts a SEED key with the provided RSA public key.

        Args:
            public_key (rsa.RSAPublicKey): RSA public key used for encryption.
            seed_key (bytes): SEED key to be encrypted.

        Returns:
            bytes: Encrypted SEED key.
        """
        try:
            encrypted_seed_key = public_key.encrypt(
                seed_key,
                padding.OAEP(
                    mgf=padding.MGF1(algorithm=hashes.SHA256()),
                    algorithm=hashes.SHA256(),
                    label=None
                )
            )
            return encrypted_seed_key
        except Exception as e:
            logging.error(f"Failed to encrypt SEED key with public key: {e}")
            raise


    def decrypt_seed_key_with_private_key(self, private_key: rsa.RSAPrivateKey, ciphertext: bytes) -> bytes:
        """
        Decrypts a ciphertext with the provided RSA private key to retrieve the SEED key.

        Args:
            private_key (rsa.RSAPrivateKey): RSA private key used for decryption.
            ciphertext (bytes): Ciphertext to be decrypted.

        Returns:
            bytes: Decrypted SEED key.
        """
        try:
            decrypted_seed_key = private_key.decrypt(
                ciphertext,
                padding.OAEP(
                    mgf=padding.MGF1(algorithm=hashes.SHA256()),
                    algorithm=hashes.SHA256(),
                    label=None
                )
            )
            return decrypted_seed_key
        except Exception as e:
            logging.error(f"Failed to decrypt SEED key with private key: {e}")
            raise