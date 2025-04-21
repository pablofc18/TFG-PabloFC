import os
from dotenv import load_dotenv
from cipher_utils import AESHelper


class LoadEntraIdData:
    def __init__(self, aes_key: bytes,):
        self.aes_key = aes_key

    # Retorna json
    def decrypt_file_to_json(self, file_enc_path: str):
        decryptor = AESHelper(self.aes_key)
        return decryptor.decrypt_file(file_enc_path)

    # Create users in Entra ID
    def create_users(self,):

    # Create groups in Entra ID
    def create_groups(self,):
    
