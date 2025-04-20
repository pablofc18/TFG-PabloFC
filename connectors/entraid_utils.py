import os
import requests
from dotenv import load_dotenv


class EntraIDUtils:
    # Utility class to help interacting with Microsoft Entra ID (& Graph API)
    def __init__(self):
        load_dotenv("../env_vars.env")
        self.tenant_id = os.getenv("TENANT_ID")
        self.graph_url = os.getenv("GRAPH_URL")
        self.login_microsoft_url = os.getenv("LOGIN_MICROSOFT_URL")
        self.client_id = os.getenv("CLIENT_ID")
        self.client_secret = os.getenv("CLIENT_SECRET")
        self.token = None
