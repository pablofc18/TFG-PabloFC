import base64
import os
import json
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend

class AESHelper:
    # Helper to encrypt/decrypt files
    def __init__(self, aes_key: bytes):
        self.aes_key = aes_key

    # Encrypt AES-CBC file
    def encrypt_file(self, dataobj, output_path: str):
        # data: dataobj
        plaintext = json.dumps(dataobj, ensure_ascii=False, indent=2).encode("utf-8")
        # padding PKCS7
        padder = padding.PKCS7(128).padder()
        padded_data = padder.update(plaintext) + padder.finalize()
        iv = os.urandom(16)
        cipher = Cipher(algorithms.AES(self.aes_key), modes.CBC(iv), backend=default_backend())
        encryptor = cipher.encryptor()
        ciphertext = encryptor.update(padded_data) + encryptor.finalize()
        # write into file
        with open(output_path, 'wb') as f:
            f.write(iv + ciphertext)

    # Decrypt file & return json
    def decrypt_file(self, input_path: str):
        # read IV + ciphertext
        with open(input_path, 'rb') as f:
            data = f.read()
        iv, ciphertext = data[:16], data[16:]
        cipher = Cipher(algorithms.AES(self.aes_key), modes.CBC(iv), backend=default_backend())
        decryptor = cipher.decryptor()
        padded_plain = decryptor.update(ciphertext) + decryptor.finalize()
        # remove  padding
        unpadder = padding.PKCS7(128).unpadder()
        plaintext = unpadder.update(padded_plain) + unpadder.finalize()
        # deserialize json
        return json.loads(plaintext.decode('utf-8'))
