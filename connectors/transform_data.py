import base64
import os
from dotenv import load_dotenv
from cipher_utils import AESHelper


class TransformOktaToEntraIdData:
    def __init__(self, entraid_domain: str, aes_key: bytes):
        self.entraid_domain = entraid_domain
        self.aes_key = base64.b64decode(aes_key)
        self.decryptor = AESHelper(self.aes_key)

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
    ## we need users already created in Entra ID to be assigned to groups
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

    # Run all, transform data from .json.enc users/groups and map to Entra Id and 
    ## save again in new json.enc 
    def run(self, users_in_enc: str, users_out_enc: str, groups_in_enc: str, groups_out_enc: str):
        # users
        raw_users = self.decryptor.decrypt_file(users_in_enc)
        mapped_users = self.map_users_to_entraid(raw_users)
        self.decryptor.encrypt_file(mapped_users, users_out_enc)
        print(f"Usuaris Entra ID xifrats a {users_out_enc}")

        # groups
        raw_groups = self.decryptor.decrypt_file(groups_in_enc)
        mapped_groups = self.map_groups_to_entraid(raw_groups)
        self.decryptor.encrypt_file(mapped_groups, groups_out_enc)
        print(f"Grups Entra ID xifrats a {groups_out_enc}")

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

    transformOktaToEntraIdData.run("users.json.enc", "users.entraid.json.enc", "groups.json.enc", "groups.entraid.json.enc")

"""     jsonobj = transformOktaToEntraIdData.decrypt_file_to_json("users.json.enc")
    print(jsonobj)
    print("\n*****\n")
    mapeigEntraid = transformOktaToEntraIdData.map_users_to_entraid(jsonobj)
    print(mapeigEntraid)
    print("\n*****\n")
    mapeigG = transformOktaToEntraIdData.map_groups_to_entraid(transformOktaToEntraIdData.decrypt_file_to_json("groups.json.enc"))
    print(mapeigG) """

