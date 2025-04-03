import requests
import os 
from dotenv import load_dotenv

load_dotenv("env_vars.env")
# Configuració: defineix el teu domini d'Okta i el teu API token
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
urlui = f'{okta_domain}/v1/userinfo'
resp = requests.get(urlui, headers=headers)
if resp.status_code == 200:
    userinfo = resp.json()
    print(userinfo)
    
else:
    print("error")