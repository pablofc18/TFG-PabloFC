import base64
import os
from dotenv import load_dotenv
from cipher_utils import AESHelper
from entraid_utils import EntraIDUtils


class TransformOktaToEntraIdData:
    def __init__(self, entraid_domain: str, aes_key: bytes, graph_url: str):
        self.entraid_domain = entraid_domain
        self.aes_key = base64.b64decode(aes_key)
        self.decryptor = AESHelper(self.aes_key)
        self.entraid_utils = EntraIDUtils()
        self.graph_url = graph_url

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
                "owners@odata.bind": [ "https://graph.microsoft.com/v1.0/users/8bfad921-68e6-4d7a-8ffa-9adb6bab57df" ], # This is the Microsoft tenant admin (me)
                "members@odata.bind": [] # will process in load_data.py
            })
        return entraid_groups

    # Add the members to each group (this method will be executed after the creation of users in Entra)
    def add_members_to_entraid_groups(self, groups_entra_json: list, groups_okta_enc_path: str, users_okta_enc_path: str, users_entra_enc_path: str) -> list:
        okta_groups = self.decryptor.decrypt_file(groups_okta_enc_path) # groups.json.enc
        entra_users = self.decryptor.decrypt_file(users_entra_enc_path) # users.entraid.json.enc
        okta_users = self.decryptor.decrypt_file(users_okta_enc_path) # users.json.enc

        # Map per cada part abans del @ del mail d'okta ens quedem amb el displayname
        ## exemple [user6@test.com -> user6: user6 user6 (=== firstName: displayName)]
        email_to_displayName = {
            usr['profile']['email']: usr['profile']['displayName']
            for usr in okta_users
        }
        # Map displayName (mateix Okta EntraID) amb userPrincipalName EntraID (email)
        displayName_to_email = {
            usr['displayName']: usr['userPrincipalName']
            for usr in entra_users
        }

        updated = []
        for grp_payload in groups_entra_json:
            name = grp_payload["displayName"]
            # troba entrada original a okta amb el mateix nom (sempre trobara, mai None)
            okta_grp = next((g for g in okta_groups if g.get("name") == name), None)
            members = []
            if okta_grp:
                for email_okta in okta_grp.get("users_list", []):
                    try:
                        print(email_okta)
                        displayName = email_to_displayName.get(email_okta)
                        if displayName:
                            email_entra = displayName_to_email.get(displayName)
                            if email_entra:
                                # obtenir id segons l'email i posar del format per entra id 
                                uid = self.entraid_utils.get_user_id(email_entra)
                                members.append(f"{self.graph_url}/v1.0/users/{uid}")
                    except Exception:
                        # si no troba continue
                        continue
            grp_payload["members@odata.bind"] = members
            updated.append(grp_payload)
        return updated

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
    GRAPH_URL = os.getenv("GRAPH_URL")

    transformOktaToEntraIdData = TransformOktaToEntraIdData(ENTRAID_DOMAIN, AES_KEY, GRAPH_URL)

    transformOktaToEntraIdData.run("users.json.enc", "users.entraid.json.enc", "groups.json.enc", "groups.entraid.json.enc")

"""     jsonobj = transformOktaToEntraIdData.decrypt_file_to_json("users.json.enc")
    print(jsonobj)
    print("\n*****\n")
    mapeigEntraid = transformOktaToEntraIdData.map_users_to_entraid(jsonobj)
    print(mapeigEntraid)
    print("\n*****\n")
    mapeigG = transformOktaToEntraIdData.map_groups_to_entraid(transformOktaToEntraIdData.decrypt_file_to_json("groups.json.enc"))
    print(mapeigG) """

