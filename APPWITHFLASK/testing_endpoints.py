import requests
import os 
from dotenv import load_dotenv

load_dotenv("../env_vars.env")
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
    print(payload)
    response = requests.post(url, data=payload)
    response.raise_for_status()
    token = response.json().get("access_token")
    if not token:
        raise RuntimeError(f"Access token no obtingut: {response.text}")
    return token


#print(get_graph_token())
OKTA_ORG_URL = os.getenv("OKTA_ORG_URL")
OKTA_DOMAIN = f"{OKTA_ORG_URL}/oauth2/default"
CLIENT_ID = os.getenv("OKTA_CLIENT_ID")
CLIENT_SECRET = os.getenv("OKTA_CLIENT_SECRET")
API_TOKEN = os.getenv("OKTA_API_TOKEN")
headers = {
    "Authorization": f"SSWS {API_TOKEN}",
    "Content-Type": "application/json"
}
# find user by eid
def find_okta_user_by_eid(eid):
    url = f"{OKTA_ORG_URL}/api/v1/users"
    parameters = {
        "search": f'profile.employeeNumber eq "{eid}"' 
    }
    response = requests.get(url, headers=headers, params=parameters)
    response.raise_for_status()
    id_user = response.json()["id"]
    return id_user if id_user else None

print(find_okta_user_by_eid("0000A"))
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
