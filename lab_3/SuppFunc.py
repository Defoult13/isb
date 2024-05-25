import logging


logging.basicConfig(level=logging.INFO)


class HelpFunc:
    """
    Utility class providing helper functions for serialization, deserialization, and file I/O.
    """

    def serialization_seed_key(self, seed_key: bytes, seed_key_path: str) -> None:
        """
        Serialize a SEED key to a file.

        Args:
            seed_key (bytes): The SEED key bytes to be serialized.
            seed_key_path (str): The path to save the serialized SEED key.
        """
        try:
            with open(seed_key_path, "wb") as seed_key_file:
                seed_key_file.write(seed_key)
            logging.info(f"SEED key serialized to {seed_key_path}")
        except Exception as e:
            logging.error(f"Failed to serialize SEED key: {e}")


    def deserialization_seed_key(self, seed_key_path: str) -> bytes:
        """
        Deserialize a SEED key from a file.

        Args:
            seed_key_path (str): The path to the file containing the serialized SEED key.

        Returns:
            bytes: The deserialized SEED key.
        """
        try:
            with open(seed_key_path, "rb") as seed_key_file:
                seed_key = seed_key_file.read()
                if len(seed_key) != 16:
                    raise ValueError("Invalid SEED key length")
                return seed_key
        except Exception as e:
            logging.error(f"Failed to deserialize SEED key: {e}")


    @classmethod           
    def write_to_file(cls, path: str, bytes_text: bytes) -> None:
        """
        Write bytes to a file.

        Args:
            path (str): The path to save the data.
            bytes_text (bytes): The bytes to write.
        """
        try:
            with open(path, "wb") as file:
                file.write(bytes_text)
            logging.info(f"Data written to {path}")
        except Exception as e:
            logging.error(f"Failed to write to file: {e}")


    @classmethod
    def read_file(cls, path: str) -> bytes:
        """
        Read bytes from a file.

        Args:
            path (str): The path to the file to be read.

        Returns:
            bytes: The bytes read from the file.
        """
        try:
            with open(path, 'rb') as file:
                return file.read()
        except Exception as e:
            logging.error(f"Failed to read file: {e}")