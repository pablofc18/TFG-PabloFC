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

    # Map Okta groups json to Entra ID groups json
    ## we need users already created in Entra ID to assign to groups
    def map_groups_to_entraid(self, groups: list) -> list:
        entraid_groups = []
        for group in groups:
            group_name = group.get("name")
            description = f"{group_name}, group for Microsoft Entra ID"

            entraid_groups.append({
                "displayName": group_name,
                "description": description,
                "groupTypes": [], # not necessary for security group in entra id
                "mailEnabled": False,
                "mailNickname": group_name,
                "securityEnabled": True,
                "owners@odata.bind": [],  # TODO
                "members@odata.bind": []  # TODO
            })
        return entraid_groups

"""
!!!app registration in group apart!!!
GROUP JSON CREATE ENTRAID
{
  "description": "Group with designated owner and members",
  "displayName": "Operations group",
  "groupTypes": [
  ],
  "mailEnabled": false,
  "mailNickname": "operations2019",
  "securityEnabled": true,
  "owners@odata.bind": [
    "https://graph.microsoft.com/v1.0/users/26be1845-4119-4801-a799-aea79d09f1a2"
  ],
  "members@odata.bind": [
    "https://graph.microsoft.com/v1.0/users/ff7cb387-6688-423c-8188-3da9532a73cc",
    "https://graph.microsoft.com/v1.0/users/69456242-0067-49d3-ba96-9de6f2728e14"
  ]
}
"""

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
    print("\n*****\n")
    mapeigG = transformOktaToEntraIdData.map_groups_to_entraid(transformOktaToEntraIdData.decrypt_file_to_json("groups.json.enc"))
    print(mapeigG)

