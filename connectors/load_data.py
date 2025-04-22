import os
import base64
import json
from dotenv import load_dotenv
from cipher_utils import AESHelper
from entraid_utils import EntraIDUtils
from transform_data import TransformOktaToEntraIdData


class LoadEntraIdData:
    def __init__(self, aes_key: bytes, entraid_domain: str, graph_url: str):
        self.aes_key = base64.b64decode(aes_key)
        self.entraid_utils = EntraIDUtils()
        self.decryptor = AESHelper(self.aes_key)
        self.transformData = TransformOktaToEntraIdData(entraid_domain, aes_key, graph_url)

    # Create users in Entra ID
    def create_users(self, users_enc_path: str, results_path: str):
        users_json = self.decryptor.decrypt_file(users_enc_path)
        batch_response = self.entraid_utils.create_users_batch(users_json)
        if results_path:
            with open(results_path, "w", encoding="utf-8") as f:
                json.dump(batch_response, f, ensure_ascii=False, indent=2)
        return batch_response

    # Create groups in Entra ID
    def create_groups(self, groups_enc_path: str, results_path: str, groups_okta_enc_path: str, users_okta_enc_path: str, users_entra_enc_path: str):
        raw_entraid_groups_no_members = self.decryptor.decrypt_file(groups_enc_path)
        # afegir una transformacio mes per afegir usuaris als grups
        groups_json = self.transformData.add_members_to_entraid_groups(raw_entraid_groups_no_members, groups_okta_enc_path, users_okta_enc_path, users_entra_enc_path)          
        batch_response = self.entraid_utils.create_groups_batch(groups_json)
        if results_path:
            with open(results_path, "w", encoding="utf-8") as f:
                json.dump(batch_response, f, ensure_ascii=False, indent=2)
        return batch_response

    # Run all, decrypt entra id json enc files and create users/groups
    def run(self, users_in_enc: str, users_out_batch: str, groups_in_enc: str, groups_out_batch: str, groups_okta_enc_path: str, users_okta_enc_path: str):
        batch_resp_u = self.create_users(users_in_enc, users_out_batch)
        batch_resp_g = self.create_groups(groups_in_enc, groups_out_batch, groups_okta_enc_path, users_okta_enc_path, users_in_enc)
        print(f"Carrega de data exitosa. Resposta json en {users_out_batch} i {groups_out_batch}")
        

if __name__ == '__main__':
    load_dotenv("../env_vars.env")
    AES_KEY = os.getenv("AES_KEY")
    ENTRAID_DOMAIN = os.getenv("ENTRAID_DOMAIN")
    GRAPH_URL = os.getenv("GRAPH_URL")
    loadData = LoadEntraIdData(AES_KEY, ENTRAID_DOMAIN, GRAPH_URL)
    loadData.run("users.entraid.json.enc", "BATCH_RESP_U.json", "groups.entraid.json.enc", "BATCH_RESP_G.json", "groups.json.enc", "users.json.enc")
    #users_res = loadData.create_users("users.json.enc", "users_batch_res.json")
    #print(json.dumps(users_res, indent=2, ensure_ascii=False))
