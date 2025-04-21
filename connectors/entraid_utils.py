import os
import requests
from dotenv import load_dotenv


class EntraIDUtils:
    # Utility class to help interacting with Microsoft Entra ID (& Graph API)
    def __init__(self):
        load_dotenv("../env_vars.env")
        self.tenant_id = os.getenv("ENTRAID_TENANT_ID")
        self.graph_url = os.getenv("GRAPH_URL")
        self.login_microsoft_url = os.getenv("LOGIN_MICROSOFT_URL")
        self.client_id = os.getenv("ENTRAID_CLIENT_ID")
        self.client_secret = os.getenv("ENTRAID_CLIENT_SECRET")
        self.token = None

    # Get uid by email
    def get_user_id(self, email: str) -> str:
        url = f"{self.graph_url}/v1.0/users/{email}"
        resp = requests.get(url, headers=self.get_headers())
        if resp.status_code != 200: # error
            raise requests.HTTPError(
                f"Error {resp.status_code} al cridar a {resp.url}: {resp.reason}"
            )
        result = resp.json().get("id", "")
        print("AAAAAAAAAAAAAAA")
        print(result)
        print("AAAAAAAAAAAAAAA")
        if not result:
            raise ValueError(f"No user found in Entra ID with email: {email}")
        return result

    # Get token for graph api
    def get_token_graph(self) -> str:
        url_graph = f"{self.login_microsoft_url}/{self.tenant_id}/oauth2/v2.0/token"
        body = {
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "scope": f"{self.graph_url}/.default",
            "grant_type": "client_credentials"
        }
        resp = requests.post(url_graph, data=body)
        if resp.status_code != 200: # error
            raise requests.HTTPError(
                f"Error {resp.status_code} al cridar a {resp.url}: {resp.reason}"
            )
        resp_json = resp.json()
        token = resp_json.get("access_token")
        if not token:
            raise ValueError("No access token found in response!!!")
        
        return token

    # Headers for requests
    def get_headers(self) -> dict:
        if not self.token:
            self.token = self.get_token_graph()
        return {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }

    # Create users (multiple per 1 request)
    def create_users_batch(self, user_payloads: list) -> dict:
        batch_url = f"{self.graph_url}/v1.0/$batch"
        requests_list = []
        for idx, payload in enumerate(user_payloads):
            requests_list.append({
                "id": str(idx),
                "method": "POST",
                "url": "/users",
                "headers": {"Content-Type": "application/json"},
                "body": payload
            })
        batch_body = {"requests": requests_list}
        resp = requests.post(batch_url, json=batch_body, headers=self.get_headers())
        if resp.status_code != 200: # error
            raise requests.HTTPError(
                f"Error {resp.status_code} al cridar a {resp.url}: {resp.reason}"
            )
        return resp.json()

    # Create groups (multple per 1 request)
    def create_groups_batch(self, group_payloads: list) -> dict:
        batch_url = f"{self.graph_url}/v1.0/$batch"
        requests_list = []
        for idx, payload in enumerate(group_payloads):
            requests_list.append({
                "id": str(idx),
                "method": "POST",
                "url": "/groups",
                "headers": {"Content-Type": "application/json"},
                "body": payload
            })
        batch_body = {"requests": requests_list}
        resp = requests.post(batch_url, json=batch_body, headers=self.get_headers())
        if resp.status_code != 200: # error
            raise requests.HTTPError(
                f"Error {resp.status_code} al cridar a {resp.url}: {resp.reason}"
            )
        print(batch_body)
        return resp.json()