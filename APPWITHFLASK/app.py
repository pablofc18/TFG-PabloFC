from flask import Flask, redirect, url_for, session
from authlib.integrations.flask_client import OAuth
from flask_sqlalchemy import SQLAlchemy
from flask.json import jsonify
import logging
import os

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY")

# conf logging
logging.basicConfig(
    level=logging.DEBUG,            
    format='[%(asctime)s] [%(levelname)s] [%(name)s] : %(message)s',
    handlers=[
        logging.FileHandler("log/flaskAppOkta.log"),
        logging.StreamHandler()
    ]
)

# DB INFO
POSTGRES = {
    'user': 'pablofc18',
    'pw': 'pablofc18', 
    'db': 'mydb',      
    'host': 'localhost',
    'port': '5432',     
}

app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql://{POSTGRES['user']}:{POSTGRES['pw']}@{POSTGRES['host']}:{POSTGRES['port']}/{POSTGRES['db']}"
# quitar notificaciones sqlalchemy
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# initialize
db = SQLAlchemy(app)

# class for table users
class User(db.Model):
    __tablename__ = 'users'
    email = db.Column(db.String(100), primary_key=True, nullable=False)
    full_name = db.Column(db.String(100), nullable=False)


# conf okta
OKTA_DOMAIN = 'https://dev-67811299.okta.com/oauth2/default'
CLIENT_ID = '0oamy75qf3BRY7URR5d7'
CLIENT_SECRET = '3s9rXnYcabFJ5SGSJ5rIUOQ8cm4tyCBsziRj6xerJCovxm1ih4zo8eMIt7bZr8Zr'

app.config['SESSION_COOKIE_NAME'] = 'okta-login-session'
# user session will end if user close browser
app.config['SESSION_PERMANENT'] = False

# conf oauth
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

# / endpoint
@app.route('/')
def home():
    user = session.get('user')
    if user:
        app.logger.info("Usuario autenticado.")
        return f'¡Hola, {user["name"]}! <br> <a href="/logout">Logout</a>'
    else:
        app.logger.info("Usuario no autenticado.")
        return '<a href="/login">Iniciar sesión con Okta</a>'

# /login endpoint
@app.route('/login')
def login():
    redirect_uri = url_for('auth', _external=True)
    nonce = os.urandom(16).hex()
    app.logger.debug(f"Asignamos nonce a la sesion actual: {nonce}")
    session['nonce'] = nonce
    app.logger.info(f"Redireccionamos a uri: {redirect_uri}")
    return okta.authorize_redirect(redirect_uri, nonce=nonce)

# /auth/callback redirect after login
@app.route('/auth/callback')
def auth():
    # 73-83 TODO: check
    token = okta.authorize_access_token()
    app.logger.info(f"Token obtenido: {token}")
    nonce = session.pop('nonce', None)  
    if not nonce:
        app.logger.error("Nonce no encontrado en la sesion!")
        return "Error: Nonce perdido o no válido", 400
    user_info = okta.parse_id_token(token, nonce)
    session['id_token'] = token.get('id_token')
    session['user'] = {
        'name': user_info['name'],
        'email': user_info['email'],
    }
    app.logger.info(f"Sesion info user: {user_info['name']}, email: {user_info['email']}")

    # guardar user si no existe en db
    existing_user = User.query.filter_by(email=user_info['email']).first()
    if not existing_user:
        app.logger.info(f"User {user_info['name']} no guardado en db")
        new_user = User(
            email=user_info['email'],
            full_name=user_info['name'],
        )
        db.session.add(new_user)
        db.session.commit()
        app.logger.info(f"User {user_info['name']} guardado en db")
    else:
        app.logger.info(f"User found in db: {existing_user.email}")

    return redirect('/')

# /logout endpoint
@app.route('/logout')
def logout():
    # cogemos id_token de la sesion
    id_token = session.pop('id_token', None)
    app.logger.info(f"Token de la sesion: {id_token}")

    # despues de logout vamos a / (home())
    logout_url = f"{OKTA_DOMAIN}/v1/logout?post_logout_redirect_uri={url_for('home', _external=True)}"
    if id_token:
        logout_url += f"&id_token_hint={id_token}"

    # clear la sesion
    session.clear()

    app.logger.info(f"Logout url: {logout_url}")
    return redirect(logout_url)

# enpoint si pagina no encontrada mostrar msj
@app.errorhandler(404)
def page_not_found(error):
    app.logger.error(error)
    return "Página no encontrada :(", 404


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)