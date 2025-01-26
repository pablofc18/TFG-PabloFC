from flask import Flask, redirect, session, request
from okta.client import Client as OktaClient
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)

# Configuración de Okta
OKTA_DOMAIN = 'https://{your-okta-domain}'
CLIENT_ID = '{your-client-id}'
CLIENT_SECRET = '{your-client-secret}'
REDIRECT_URI = 'http://192.168.1.10:5000/authorization-code/callback'

okta_client = OktaClient({
    'orgUrl': OKTA_DOMAIN,
    'token': '{your-api-token}'
})

@app.route('/')
def home():
    if 'user' in session:
        return '¡Estás loggeado!'
    else:
        return '<a href="/login">Iniciar sesión con Okta</a>'

@app.route('/login')
def login():
    # Redirige al usuario a la página de login de Okta
    auth_url = f"{OKTA_DOMAIN}/oauth2/default/v1/authorize?client_id={CLIENT_ID}&response_type=code&scope=openid profile&redirect_uri={REDIRECT_URI}&state=state-123"
    return redirect(auth_url)

@app.route('/authorization-code/callback')
def callback():
    # Intercambia el código de autorización por un token de acceso
    code = request.args.get('code')
    token_url = f"{OKTA_DOMAIN}/oauth2/default/v1/token"
    data = {
        'grant_type': 'authorization_code',
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'code': code,
        'redirect_uri': REDIRECT_URI
    }
    response = requests.post(token_url, data=data)
    token = response.json().get('access_token')

    # Almacena el token en la sesión
    session['user'] = token
    return redirect('/')

@app.route('/logout')
def logout():
    # Cierra la sesión
    session.pop('user', None)
    return redirect('/')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)