import json
import base64
import os
from dotenv import load_dotenv
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cipher_utils import AESHelper


class TransformOktaToEntraIdData:
    def __init__(self, aes_key: str):
        self.aes_key = base64.b64decode(aes_key)

    # Retorna json
    def decrypt_file_to_json(self, file_enc_path: str):
        decryptor = AESHelper(self.aes_key)
        return decryptor.decrypt_file(file_enc_path)

    # Map Okta users json to Entra ID users json
    def map_users_to_entraid(self, users: list):
        return True
"""
To create user json example MICROSOFT ENTRA ID
{
  "accountEnabled": true,
  "displayName": "Adele Vance",
  "mailNickname": "AdeleV",
  "userPrincipalName": "AdeleV@contoso.com",
  "employeeId": "0000X"
  "passwordProfile" : {
    "forceChangePasswordNextSignIn": true,
    "password": "xWwvJ]6NMw+bWH-d"
  }
}
"""

if __name__ == '__main__':
    load_dotenv("../env_vars.env")
    AES_KEY = os.getenv("AES_KEY")  

    if not AES_KEY:
        raise ValueError("Defineix AES_KEY a env_vars.env!!!")

    transformOktaToEntraIdData = TransformOktaToEntraIdData(AES_KEY)
    jsonobj = transformOktaToEntraIdData.decrypt_file_to_json("users.json.enc")
    print(jsonobj)

