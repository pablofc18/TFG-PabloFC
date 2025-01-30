from flask import Flask, redirect, url_for, session
from authlib.integrations.flask_client import OAuth
from flask_sqlalchemy import SQLAlchemy
from flask.json import jsonify
import os

app = Flask(__name__)
app.secret_key = 'probandoaversifucnionadeunavez$$$!!!'

# DB INFO
POSTGRES = {
    'user': 'pablofc18',
    'pw': 'pablofc18', 
    'db': 'mydb',      
    'host': 'localhost',
    'port': '5432',     
}

app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql://{POSTGRES['user']}:{POSTGRES['pw']}@{POSTGRES['host']}:{POSTGRES['port']}/{POSTGRES['db']}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# initialize
db = SQLAlchemy(app)

# class for table users
class User(db.Model):
    __tablename__ = 'users'
    email = db.Column(db.String(100), primary_key=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)


# Configuración de Okta
OKTA_DOMAIN = 'https://dev-67811299.okta.com/oauth2/default'
CLIENT_ID = '0oamy75qf3BRY7URR5d7'
CLIENT_SECRET = '3s9rXnYcabFJ5SGSJ5rIUOQ8cm4tyCBsziRj6xerJCovxm1ih4zo8eMIt7bZr8Zr'

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
    session['id_token'] = token.get('id_token')
    session['user'] = {
        'name': user_info['name'],
        'email': user_info['email'],
    }

    # Guardar user si no existe
    existing_user = User.query.filter_by(email=user_info['email']).first()
    if not existing_user:
        new_user = User(
            email=user_info['email'],
            name=user_info['name'],
        )
        db.session.add(new_user)
        db.session.commit()

    return redirect('/')

# Ruta para cerrar sesión
@app.route('/logout')
def logout():
    # Obtén el id_token de la sesión
    id_token = session.pop('id_token', None)

    # Construye la URL de cierre de sesión de Okta
    logout_url = f"{OKTA_DOMAIN}/v1/logout?post_logout_redirect_uri={url_for('home', _external=True)}"
    if id_token:
        logout_url += f"&id_token_hint={id_token}"

    # Limpia la sesión del usuario
    session.clear()

    # Redirige al usuario al URL de cierre de sesión
    return redirect(logout_url)

@app.errorhandler(404)
def page_not_found(error):
    return "Página no encontrada", 404


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)