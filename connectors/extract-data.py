from dotenv import load_dotenv
import base64
import os
import requests

class ExtractOktaData:
    def __init__(self, org_url: str, api_token: str, aes_key: bytes):
        self.org_url = org_url
        self.api_token = api_token
        self.aes_key = aes_key
        self.headers = {
            "Authorization": f"SSWS {self.api_token}",
            "Content-Type": "application/json"
        }

    # Extract user info in Okta users endpoint
    def extract_users(self):
        url = f"{self.org_url}/api/v1/users"
        resp = requests.get(url, headers=self.headers)
        if resp.status_code != 200: # error
            raise requests.HTTPError(
                f"Error {resp.status_code} al cridar a {resp.url}: {resp.reason}"
            )
        
        raw_users = resp.json()
        simplified_users = []
        #for user in raw_users:
        print (raw_users)
        with open("testOUTPUT.json", "w") as f:
            f.write(raw_users)




if __name__ == '__main__':
    # load env vars (per protegir credencials)
    load_dotenv("../env_vars.env")
    OKTA_ORG_URL = os.getenv("OKTA_ORG_URL")
    OKTA_API_TOKEN = os.getenv("OKTA_API_TOKEN")
    AES_KEY = os.getenv("AES_KEY")

    if not OKTA_API_TOKEN or not AES_KEY:
        raise ValueError("Env vars okta api token i aes key HAN D'ESTAR DEFINIDES")

    extractOktaData = ExtractOktaData(OKTA_ORG_URL, OKTA_API_TOKEN, AES_KEY)
    extractOktaData.extract_users()



