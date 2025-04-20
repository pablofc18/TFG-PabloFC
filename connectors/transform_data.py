import json
import base64
import os
from dotenv import load_dotenv
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend

class TransformOktaData:
    def __init__(self, aes_key: str):
        self.aes_key = base64.b64decode(aes_key)

    # Decrypt file into json
    def decrypt_file(self, input_path: str):
        with open(input_path, 'rb') as f:
            data = f.read()
        # Extract IV && encrypted
        iv = data[:16]
        ciphertext = data[16:]

        # decrypt
        cipher = Cipher(algorithms.AES(self.aes_key), modes.CBC(iv), backend=default_backend())
        decryptor = cipher.decryptor()
        padded_plain = decryptor.update(ciphertext) + decryptor.finalize()

        # remove padding 
        unpadder = padding.PKCS7(128).unpadder()
        plain = unpadder.update(padded_plain) + unpadder.finalize()

        # Load JSON
        return json.loads(plain.decode('utf-8'))

    def decrypt_users(self, users_enc_path: str = 'users.json.enc'):
        """
        Desxifra i retorna la llista d'usuaris.
        """
        return self._decrypt_file(users_enc_path)

    def decrypt_groups(self, groups_enc_path: str = 'groups.json.enc'):
        """
        Desxifra i retorna la llista de grups.
        """
        return self._decrypt_file(groups_enc_path)

    def run(self,
            users_enc_path: str = 'users.json.enc',
            groups_enc_path: str = 'groups.json.enc'):
        """
        Desxifra usuaris i grups i els mostra per pantalla.
        """
        users = self.decrypt_users(users_enc_path)
        groups = self.decrypt_groups(groups_enc_path)

        print("Usuaris desxifrats:")
        print(json.dumps(users, indent=2, ensure_ascii=False))
        print("\nGrups desxifrats:")
        print(json.dumps(groups, indent=2, ensure_ascii=False))

if __name__ == '__main__':
    load_dotenv("../env_vars.env")
    AES_KEY = os.getenv("AES_KEY")  

    if not AES_KEY:
        raise ValueError("Defineix AES_KEY a env_vars.env!!!")

    transformer = TransformOktaData(AES_KEY)
    transformer.run()
