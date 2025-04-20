import json
import base64
import os
from dotenv import load_dotenv
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cipher_utils import AESHelper


class TransformOktaToEntraIdData:
    def __init__(self, entraid_domain: str, aes_key: str):
        self.entraid_domain = entraid_domain
        self.aes_key = base64.b64decode(aes_key)

    # Retorna json
    def decrypt_file_to_json(self, file_enc_path: str):
        decryptor = AESHelper(self.aes_key)
        return decryptor.decrypt_file(file_enc_path)

    # Map Okta users json to Entra ID users json
    def map_users_to_entraid(self, users: list) -> list:
        entraid_users_format = []
        for user in users:
            profile = user.get("profile", {})
            displayName = profile.get("displayName")
            nickname = "".join(displayName.split()) 
            email = f"{nickname}@{self.entraid_domain}" # new mail (microsoft entra id org)

            entraid_users_format.append({
                "accountEnabled": True,
                "displayName": displayName,
                "mailNickname": nickname,
                "userPrincipalName": email,
                "employeeId": profile.get("employeeNumber"),
                "passwordProfile": {
                    "forceChangePasswordNextSignIn": True,
                    "password": "Prueba123!"
                }
            })
        return entraid_users_format


if __name__ == '__main__':
    load_dotenv("../env_vars.env")
    AES_KEY = os.getenv("AES_KEY")  
    ENTRAID_DOMAIN = os.getenv("ENTRAID_DOMAIN")

    transformOktaToEntraIdData = TransformOktaToEntraIdData(ENTRAID_DOMAIN, AES_KEY)
    jsonobj = transformOktaToEntraIdData.decrypt_file_to_json("users.json.enc")
    print(jsonobj)
    print("\n*****\n")
    mapeigEntraid = transformOktaToEntraIdData.map_users_to_entraid(jsonobj)
    print(mapeigEntraid)

