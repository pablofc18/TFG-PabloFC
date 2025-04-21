import os
import base64
import json
from dotenv import load_dotenv
from cipher_utils import AESHelper
from entraid_utils import EntraIDUtils


class LoadEntraIdData:
    def __init__(self, aes_key: bytes):
        self.aes_key = base64.b64decode(aes_key)
        self.entraid_utils = EntraIDUtils()
        self.decryptor = AESHelper(self.aes_key)

    # Create users in Entra ID
    def create_users(self, users_enc_path: str, results_path: str):
        users_json = self.decryptor.decrypt_file(users_enc_path)
        batch_response = self.entraid_utils.create_users_batch(users_json)
        if results_path:
            with open(results_path, "w", encoding="utf-8") as f:
                json.dump(batch_response, f, ensure_ascii=False, indent=2)
        return batch_response

    # Create groups in Entra ID
    #def create_groups(self,):

if __name__ == '__main__':
    load_dotenv("../env_vars.env")
    AES_KEY = os.getenv("AES_KEY")
    loadData = LoadEntraIdData(AES_KEY)
    users_res = loadData.create_users("users.json.enc", "users_batch_res.json")
    print(json.dumps(users_res, indent=2, ensure_ascii=False))
