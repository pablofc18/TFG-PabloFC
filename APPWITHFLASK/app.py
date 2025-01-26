from flask import Flask, redirect, url_for, session
from authlib.integrations.flask_client import OAuth
from flask.json import jsonify
import os

app = Flask(__name__)
app.secret_key = 'probandoaversifucnionadeunavez$$$!!!'

# Configuración de Okta
OKTA_DOMAIN = 'https://dev-67811299.okta.com/oauth2/default'
CLIENT_ID = '0oamy75qf3BRY7URR5d7'
CLIENT_SECRET = '3s9rXnYcabFJ5SGSJ5rIUOQ8cm4tyCBsziRj6xerJCovxm1ih4zo8eMIt7bZr8Zr'
REDIRECT_URI = 'http://192.168.1.10:5000/authorization-code/callback'

app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SESSION_COOKIE_NAME'] = 'okta-login-session'
app.config['SESSION_PERMANENT'] = False

# Configuración de Authlib
oauth = OAuth(app)
okta = oauth.register(
    name='okta',
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    server_metadata_url=f'{OKTA_DOMAIN}/.well-known/openid-configuration',
    client_kwargs={
        'scope': 'openid profile email',
    }
)

# Ruta principal
@app.route('/')
def home():
    user = session.get('user')
    if user:
        return f'¡Hola, {user["name"]}!'
    else:
        return '<a href="/login">Iniciar sesión con Okta</a>'

# Ruta para iniciar sesión
@app.route('/login')
def login():
    redirect_uri = url_for('auth', _external=True)
    nonce = os.urandom(16).hex()
    session['nonce'] = nonce
    return okta.authorize_redirect(redirect_uri, nonce=nonce)

# Ruta de redirección después del inicio de sesión
@app.route('/auth/callback')
def auth():
    token = okta.authorize_access_token()
    nonce = session.pop('nonce', None)  # Recupera y elimina el nonce de la sesión
    if not nonce:
        return "Error: Nonce perdido o no válido", 400
    # Valida el ID Token con el nonce
    user_info = okta.parse_id_token(token, nonce=nonce)
    session['user'] = {
        'name': user_info['name'],
        'email': user_info['email'],
    }
    return redirect('/')

# Ruta para cerrar sesión
@app.route('/logout')
def logout():
    session.pop('user', None)
    logout_url = f"{OKTA_DOMAIN}/v1/logout?id_token_hint={session.get('id_token')}&post_logout_redirect_uri={url_for('home', _external=True)}"
    return redirect(logout_url)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)