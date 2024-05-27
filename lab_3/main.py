import os
import argparse
import logging
import json

from cryptography.hazmat.primitives import serialization

from asymm_crypt import AsymmCrypt
from symm_crypt import SymmCrypt
from SuppFunc import HelpFunc


logging.basicConfig(level=logging.INFO)


def main(config_path, operation):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(script_dir, "config.json")
    try:
        with open(config_path, "r") as file:
            config = json.load(file)
    except FileNotFoundError:
        logging.error(f"Configuration file not found: {config_path}")
        return
    except json.JSONDecodeError:
        logging.error(f"Error decoding JSON from the configuration file: {config_path}")
        return
    except Exception as e:
        logging.error(f"Unexpected error reading configuration file: {e}")
        return
    if operation:
        config["operation"] = operation
    match config["operation"]:
        case "generate_rsa_keys":
            asymm_crypt = AsymmCrypt()
            private_key, public_key = asymm_crypt.generate_key_pair()
            private_key_pem = private_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.PKCS8,
                encryption_algorithm=serialization.NoEncryption()
            )
            public_key_pem = public_key.public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo
            )
            HelpFunc.write_to_file(config["private_key_path"], private_key_pem)
            HelpFunc.write_to_file(config["public_key_path"], public_key_pem)
            logging.info("RSA key pair generated and saved.")

        case "generate_seed_key":
            symm_crypt = SymmCrypt(key_len=128)
            seed_key = symm_crypt.generate_key()
            asymm_crypt = AsymmCrypt()
            public_key_pem = HelpFunc.read_file(config["public_key_path"])
            if not public_key_pem:
                logging.error("Public key file is empty or not found.")
            public_key = serialization.load_pem_public_key(public_key_pem)
            encrypted_seed_key = asymm_crypt.encrypt_seed_key_with_public_key(public_key, seed_key)
            HelpFunc.write_to_file(config["encrypted_seed_key_path"], encrypted_seed_key)
            logging.info("SEED key generated and saved.")

        case "encrypt_text":
            try:
                private_key_pem = HelpFunc.read_file(config["private_key_path"])
                if not private_key_pem:
                    logging.error("Private key file is empty or not found.")
                private_key = serialization.load_pem_private_key(private_key_pem, password=None)
                encrypted_seed_key = HelpFunc.read_file(config["encrypted_seed_key_path"])
                if not encrypted_seed_key:
                    logging.error("Encrypted SEED key file is empty or not found.")
                asymm_crypt = AsymmCrypt()
                decrypted_seed_key = asymm_crypt.decrypt_seed_key_with_private_key(private_key, encrypted_seed_key)
                text_to_encrypt = HelpFunc.read_file(config["text_path"])
                symm_crypt = SymmCrypt(key_len=128)
                symm_crypt.encrypt_text(decrypted_seed_key, config["encrypted_text_path"], config["iv_path"], text_to_encrypt)
                logging.info("Text encrypted and saved.")
            except Exception as e:
                logging.error(f"Error during text encryption: {e}")

        case "decrypt_text":
            try:
                encrypted_seed_key = HelpFunc.read_file(config["encrypted_seed_key_path"])
                if not encrypted_seed_key:
                    logging.error("Encrypted SEED key file is empty or not found.")
                private_key_pem = HelpFunc.read_file(config["private_key_path"])
                if not private_key_pem:
                    logging.error("Private key file is empty or not found.")
                private_key = serialization.load_pem_private_key(private_key_pem, password=None)
                asymm_crypt = AsymmCrypt()
                decrypted_seed_key = asymm_crypt.decrypt_seed_key_with_private_key(private_key, encrypted_seed_key)
                symm_crypt = SymmCrypt(key_len=128)
                symm_crypt.decrypt_text(decrypted_seed_key, config["decrypted_text_path"], config["iv_path"], config["encrypted_text_path"])
                logging.info("Text decrypted and saved.")
            except Exception as e:
                logging.error(f"Error during text decryption: {e}")

        case _:
            logging.error(f"Unknown operation: {config['operation']}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process some cryptographic operations.")
    parser.add_argument("--config_path", type=str, default= os.path.join("K", "Pyth", "ISB", "isb", "lab_3", "config.json"), help="Path to the JSON configuration file.")
    parser.add_argument("--operation", type=str, default= "decrypt_text", help="Operation to perform (overrides the operation in the config file).")
    args = parser.parse_args()
    main(args.config_path, args.operation)