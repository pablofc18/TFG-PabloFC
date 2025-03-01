from flask import Flask, redirect, url_for, session, render_template, request, flash
from authlib.integrations.flask_client import OAuth
from flask_sqlalchemy import SQLAlchemy
from flask.json import jsonify
import requests
import logging
import os

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY")

# conf logging
logging.basicConfig(
    level=logging.DEBUG,            
    format="[%(asctime)s] [%(levelname)s] [%(name)s] : %(message)s",
    handlers=[
        logging.FileHandler("log/flaskAppOkta.log"),
        logging.StreamHandler()
    ]
)

# DB INFO
POSTGRES = {
    "user": "pablofc18",
    "pw": "pablofc18", 
    "db": "mydb",      
    "host": "localhost",
    "port": "5432",     
}

app.config["SQLALCHEMY_DATABASE_URI"] = f"postgresql://{POSTGRES["user"]}:{POSTGRES["pw"]}@{POSTGRES["host"]}:{POSTGRES["port"]}/{POSTGRES["db"]}"
# quitar notificaciones sqlalchemy
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
# initialize
db = SQLAlchemy(app)

# class for table users
class User(db.Model):
    __tablename__ = "users"
    email = db.Column(db.String(100), primary_key=True, nullable=False)
    full_name = db.Column(db.String(100), nullable=False)


# conf okta
OKTA_ORG_URL = "https://dev-67811299.okta.com" 
OKTA_DOMAIN = f"{OKTA_ORG_URL}/oauth2/default"
CLIENT_ID = "0oamy75qf3BRY7URR5d7"
CLIENT_SECRET = "3s9rXnYcabFJ5SGSJ5rIUOQ8cm4tyCBsziRj6xerJCovxm1ih4zo8eMIt7bZr8Zr"
API_TOKEN = "00nH4N4nc-V9u7Io4kofmaXlUPIHrljtW4NiiMCklp" 

app.config["SESSION_COOKIE_NAME"] = "okta-login-session"
# user session will end if user close browser
app.config["SESSION_PERMANENT"] = False

# conf oauth
oauth = OAuth(app)
okta = oauth.register(
    name="okta",
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    server_metadata_url=f"{OKTA_DOMAIN}/.well-known/openid-configuration",
    client_kwargs={
        "scope": "openid profile email",
    }
)

###
### Api calls methods
###
# find id with email
def get_okta_user_id(email):
    headers = {
        "Authorization": f"SSWS {API_TOKEN}",
        "Content-Type": "application/json"
    }
    response = requests.get(f"{OKTA_ORG_URL}/api/v1/users/{email}", headers=headers)
    if response.status_code == 200:
        id_user = response.json()["id"]
        app.logger.info(f"Id de l'usuari: {id_user}")
        return id_user
    else:
        app.logger.error(f"Error obtenint usuari d'Okta: {response.text}")
        return None

# modif profile in Okta
# @param user_id -> id
# @param profile_data -> new profile to modif in Okta
def update_okta_user_profile(user_id, profile_data):
    headers = {
        'Authorization': f'SSWS {API_TOKEN}',
        'Content-Type': 'application/json'
    }
    data = {
        "profile": profile_data
    }
    response = requests.post(f"{OKTA_ORG_URL}/api/v1/users/{user_id}", headers=headers, json=data)
    if response.status_code == 200:
        app.logger.info(f"Perfil d'Okta actualitzat correctament: {profile_data}")
        return True
    else:
        app.logger.error(f"Error actualitzant perfil d'usuari a Okta: {response.text}")
        return False

### 
### ENDPOINTS
###
# / endpoint
@app.route("/")
def home():
    user = session.get("user")
    if user:
        app.logger.info("Usuari autenticat.")
        return render_template("home.html", user=user)
    else:
        app.logger.info("Usuari no autenticat.")
        return render_template("home.html", user=user)

# /login endpoint
@app.route("/login")
def login():
    redirect_uri = url_for("auth", _external=True)
    nonce = os.urandom(16).hex()
    app.logger.debug(f"Asignem nonce a la sessio actual: {nonce}")
    session["nonce"] = nonce
    app.logger.info(f"Redireccionem a uri: {redirect_uri}")
    return okta.authorize_redirect(redirect_uri, nonce=nonce)

# /auth/callback redirect after login
@app.route("/auth/callback")
def auth():
    # 73-83 TODO: check
    token = okta.authorize_access_token()
    app.logger.info(f"Token obtingut: {token}")
    nonce = session.pop("nonce", None)  
    if not nonce:
        app.logger.error("Nonce no trobat en la sessio!")
        return "Error: Nonce perdut o no valid", 400
    user_info = okta.parse_id_token(token, nonce)
    session["id_token"] = token.get("id_token")
    session["user"] = {
        "name": user_info["name"],
        "email": user_info["email"],
    }
    app.logger.info(f"Sessio info usuari: {user_info["name"]}, email: {user_info["email"]}")

    # guardar user si no existe en db
    existing_user = User.query.filter_by(email=user_info["email"]).first()
    if not existing_user:
        app.logger.info(f"User {user_info["name"]} no guardat en db")
        new_user = User(
            email=user_info["email"],
            full_name=user_info["name"],
        )
        db.session.add(new_user)
        db.session.commit()
        app.logger.info(f"User {user_info["name"]} guardat en db")
    else:
        app.logger.info(f"User trobat in db: {existing_user.email}")

    return redirect("/")

# /profile endpoint per veure i editar el perfil
@app.route("/profile")
def profile():
    user = session.get("user")
    if not user:
        app.logger.warning("Usuari perdut al intentar modificar perfil!")
        return redirect("/login")
    
    db_user = User.query.filter_by(email=user["email"]).first()
    app.logger.info(f"User a modifcar: {db_user}")
    return render_template("profile.html", user=db_user)

# /update_profile per modificar el perfil
@app.route('/update_profile', methods=['POST'])
def update_profile():
    user = session.get('user')
    app.logger.info(f"user:{user}")
    if not user:
        return redirect('/login')
    
    # dades del formulari
    full_name = request.form.get('full_name')
    app.logger.info(f"full_name: {full_name}")
    app.logger.info(f"email: {user.email}")
    
    # si no modifica full_name torna a profile
    if not full_name:
        return redirect('/profile')
    
    # Obtenir l'usuari actual de la base de dades
    current_user = User.query.filter_by(email=user['email']).first()
    if not current_user:
        flash('Usuari no trobat', 'danger')
        return redirect('/profile')
    
    try:
        # Actualitzar l'usuari a Okta
        okta_user_id = get_okta_user_id(user.email)
        app.logger.info(f"okta_user_id: {okta_user_id}")
        if okta_user_id:
            profile_data = {
                "firstName": full_name.split()[0],
                "lastName": ' '.join(full_name.split()[1:]) if len(full_name.split()) > 1 else "",
                "email": user.email,
                "login": user.email,
                "displayName": full_name
            }
            if update_okta_user_profile(okta_user_id, profile_data):
                # Si actualitzacio a Okta exit, actualitzar la BD 
                current_user.full_name = full_name
                
                db.session.commit()
                
                # Actualitzar la sessió
                session['user'] = {
                    'name': full_name,
                    'email': email,
                }
                
                flash('Perfil actualitzat correctament', 'success')
            else:
                flash('Error en actualitzar el perfil a Okta', 'danger')
        else:
            flash('No s\'ha pogut trobar l\'usuari a Okta', 'danger')
    except Exception as e:
        db.session.rollback()
        app.logger.error(f"Error en actualitzar el perfil: {str(e)}")
        flash(f'Error en actualitzar el perfil: {str(e)}', 'danger')
    
    return redirect('/profile')

# /logout endpoint
@app.route("/logout")
def logout():
    # cogemos id_token de la sesion
    id_token = session.pop("id_token", None)
    app.logger.info(f"Token de la sessio: {id_token}")

    # despues de logout vamos a / (home())
    logout_url = f"{OKTA_DOMAIN}/v1/logout?post_logout_redirect_uri={url_for("home", _external=True)}"
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
    return "Pagina no trobada. ERROR 404 :(", 404


###
### MAIN
###
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)