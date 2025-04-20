import json
import base64
import os
import requests
from dotenv import load_dotenv
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cipher_utils import AESHelper


class ExtractOktaData:
    def __init__(self, org_url: str, api_token: str, aes_key: bytes):
        self.org_url = org_url
        self.api_token = api_token
        self.aes_key = base64.b64decode(aes_key)
        self.headers = {
            "Authorization": f"SSWS {self.api_token}",
            "Content-Type": "application/json"
        }

    # Extract user info in Okta users endpoint
    def extract_users_info(self):
        url = f"{self.org_url}/api/v1/users"
        resp = requests.get(url, headers=self.headers)
        if resp.status_code != 200: # error
            raise requests.HTTPError(
                f"Error {resp.status_code} al cridar a {resp.url}: {resp.reason}"
            )
        raw_users = resp.json()

        simplified_users = []
        for user in raw_users:
            profile = user.get("profile", {})
            simplified_users.append({
                "id": user.get("id"),
                "profile": {
                    "firstName": profile.get("firstName"),
                    "lastName": profile.get("lastName"),
                    "displayName": profile.get("displayName"),
                    "login": profile.get("login"), # login and email are the same
                    "email": profile.get("email"),
                    "employeeNumber": profile.get("employeeNumber")
                }
            })
        return simplified_users

    # Extract group info in Okta groups endpoint (id, name, users_list, apps_list)
    def extract_groups_info(self):
        url = f"{self.org_url}/api/v1/groups"
        resp = requests.get(url, headers=self.headers)
        if resp.status_code != 200: # error
            raise requests.HTTPError(
                f"Error {resp.status_code} al cridar a {resp.url}: {resp.reason}"
            )
        raw_groups = resp.json()

        simplified_groups = []
        for group in raw_groups:
            # filter by groups created by me
            if group.get("type") != "OKTA_GROUP":
                continue

            group_id = group.get("id")
            group_name = group.get("profile", {}).get("name")

            # get users email list
            users_url = group.get("_links", {}).get("users", {}).get("href")
            users_email = []
            if users_url: 
                raw_users = requests.get(users_url, headers=self.headers)
                if raw_users.status_code != 200: # error
                    raise requests.HTTPError(
                        f"Error {resp.status_code} al cridar a {resp.url}: {resp.reason}"
                    )
                users_json = raw_users.json() 
                users_email = [
                    user.get("profile", {}).get("email")
                    for user in users_json
                    if isinstance(user, dict)
                ]
            
            # get asigned apps name list
            apps_url = group.get("_links", {}).get("apps", {}).get("href")
            apps_name = []
            if apps_url:
                raw_apps = requests.get(apps_url, headers=self.headers)
                if resp.status_code != 200: # error
                    raise requests.HTTPError(
                        f"Error {resp.status_code} al cridar a {resp.url}: {resp.reason}"
                    )
                apps_json = raw_apps.json()
                apps_name = [app.get("label") for app in apps_json]
            
            simplified_groups.append({
                "id": group_id,
                "name": group_name,
                "users_list": users_email,
                "apps_list": apps_name
            })
        return simplified_groups

    # Run all, extract data (2 files: groups and users) and save encrypted .json 
    def run(self, users_enc_path: str, groups_enc_path: str):
        # cipher utils
        encryptor = AESHelper(self.aes_key)
        # users
        users = self.extract_users_info()
        encryptor.encrypt_file(users, users_enc_path)
        # groups
        groups = self.extract_groups_info()
        encryptor.encrypt_file(groups, groups_enc_path)
        # show msg in terminal
        print(f"Usuaris i grups exportats i xifrats en: {users_enc_path} && {groups_enc_path}")


if __name__ == '__main__':
    # load env vars (per protegir credencials)
    load_dotenv("../env_vars.env")
    OKTA_ORG_URL = os.getenv("OKTA_ORG_URL")
    OKTA_API_TOKEN = os.getenv("OKTA_API_TOKEN")
    AES_KEY = os.getenv("AES_KEY")

    if not OKTA_API_TOKEN or not AES_KEY:
        raise ValueError("Env vars okta api token i aes key HAN D'ESTAR DEFINIDES")

    extractOktaData = ExtractOktaData(OKTA_ORG_URL, OKTA_API_TOKEN, AES_KEY)
    extractOktaData.run("users.json.enc", "groups.json.enc")



