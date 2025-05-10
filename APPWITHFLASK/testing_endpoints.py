import requests
import os 
from dotenv import load_dotenv

load_dotenv("env_vars.env")
# conf entra id
ENTRAID_TENANT_ID     = os.getenv("ENTRAID_TENANT_ID")
ENTRAID_CLIENT_ID     = os.getenv("ENTRAID_CLIENT_ID")
ENTRAID_CLIENT_SECRET = os.getenv("ENTRAID_CLIENT_SECRET")
ENTRAID_AUTHORITY     = f"{os.getenv("LOGIN_MICROSOFT_URL")}/{ENTRAID_TENANT_ID}"
ENTRAID_OPENID_CONFIG = f"{ENTRAID_AUTHORITY}/v2.0/.well-known/openid-configuration"
GRAPH_URL             = os.getenv("GRAPH_URL")
def get_graph_token():
    url = f"{ENTRAID_AUTHORITY}/oauth2/v2.0/token"
    payload = {
        "grant_type": "client_credentials",
        "client_id": ENTRAID_CLIENT_ID,
        "client_secret": ENTRAID_CLIENT_SECRET,
        "scope": f"{GRAPH_URL}/.default"
    }
    response = requests.post(url, json=payload)
    response.raise_for_status()
    token = response.json().get("access_token")
    if not token:
        raise RuntimeError(f"Access token no obtingut: {response.text}")
    return token

print(get_graph_token())
"""
okta_domain = os.getenv("OKTA_ORG_URL")
api_token = os.getenv("OKTA_API_TOKEN")
headers = {
    'Authorization': f'SSWS {api_token}',
    'Accept': 'application/json'
}

# Exemple: Obtenir usuaris i mostrar els seus atributs
url_users = f'{okta_domain}/api/v1/users'
response_users = requests.get(url_users, headers=headers)

if response_users.status_code == 200:
    usuaris = response_users.json()
    for usuari in usuaris:
        # Obtenim el perfil de l'usuari, on es troben els atributs
        profile = usuari.get('profile', {})
        print("Atributs de l'usuari:")
        for clau, valor in profile.items():
            print(f"{clau}: {valor}")
        print("-" * 40)
else:
    print("Error en obtenir els usuaris:", response_users.status_code, response_users.text)

print("***********************************")
print("***********************************")
print("***********************************")
print("***********************************")
print("***********************************")
### userinfo endpoint
headers = {
    'Authorization': f'Bearer {api_token}',
    'Accept': 'application/json'
}
urlui = f'{okta_domain}/v1/userinfo'
resp = requests.get(urlui, headers=headers)
if resp.status_code == 200:
    userinfo = resp.json()
    print(userinfo)
    
else:
    print("error")
"""