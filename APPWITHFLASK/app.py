from flask import Flask, redirect, url_for, session, render_template, request, flash
from authlib.integrations.flask_client import OAuth
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
from functools import wraps
import base64 
import json
import requests
import logging
import os
import re

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY") # variable not in file (os env system)

# load env vars (per protegir credencials)
load_dotenv("../env_vars.env")

# conf logging
logging.basicConfig(
    level=logging.DEBUG,            
    format="[%(asctime)s] [%(levelname)s] [%(name)s] : %(message)s",
    handlers=[
        logging.FileHandler("log/flaskAppOkta.log"),
        logging.StreamHandler() # tambe mostrara log en terminal
    ]
)

# db info
POSTGRES = {
    "user": os.getenv("POSTGRES_USER"),
    "pw": os.getenv("POSTGRES_PW"), 
    "db": os.getenv("POSTGRES_DB"),
    "host": os.getenv("POSTGRES_HOST"),
    "port": os.getenv("POSTGRES_PORT", "5432"),
}

app.config["SQLALCHEMY_DATABASE_URI"] = f"postgresql://{POSTGRES["user"]}:{POSTGRES["pw"]}@{POSTGRES["host"]}:{POSTGRES["port"]}/{POSTGRES["db"]}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False # quitar notificaciones sqlalchemy
# initialize
db = SQLAlchemy(app)

# class for table users
# (no es pot guardar contrsenya d'Okta a db)
class User(db.Model):
    __tablename__ = "users"
    email = db.Column(db.String(100), primary_key=True, nullable=False)
    full_name = db.Column(db.String(100), nullable=False)
    eid = db.Column(db.String(5), nullable=False)


# conf okta
OKTA_ORG_URL = os.getenv("OKTA_ORG_URL")
OKTA_DOMAIN = f"{OKTA_ORG_URL}/oauth2/default"
CLIENT_ID = os.getenv("OKTA_CLIENT_ID")
CLIENT_SECRET = os.getenv("OKTA_CLIENT_SECRET")
API_TOKEN = os.getenv("OKTA_API_TOKEN")

app.config["SESSION_COOKIE_NAME"] = "login-session"
app.config["SESSION_PERMANENT"] = False # user session terminara si es tanca navegador 

# conf oauth Okta
oauth = OAuth(app)
okta_oauth = oauth.register(
    name="okta",
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    server_metadata_url=f"{OKTA_DOMAIN}/.well-known/openid-configuration",
    client_kwargs={
        "scope": "openid profile email",
    }
)

# conf entra id
ENTRAID_TENANT_ID     = os.getenv("ENTRAID_TENANT_ID")
ENTRAID_CLIENT_ID     = os.getenv("ENTRAID_CLIENT_ID")
ENTRAID_CLIENT_SECRET = os.getenv("ENTRAID_CLIENT_SECRET")
ENTRAID_AUTHORITY     = f"{os.getenv("LOGIN_MICROSOFT_URL")}/{ENTRAID_TENANT_ID}"
ENTRAID_OPENID_CONFIG = f"{ENTRAID_AUTHORITY}/v2.0/.well-known/openid-configuration"
GRAPH_URL             = os.getenv("GRAPH_URL")

# conf oauth Entra id
entraid_oauth = oauth.register(
    name="microsoft",
    client_id=ENTRAID_CLIENT_ID,
    client_secret=ENTRAID_CLIENT_SECRET,
    server_metadata_url=ENTRAID_OPENID_CONFIG,
    client_kwargs={
        "scope": "openid profile email api://myAppFlask/myApp-scope" # TODO CHECK SCOPES!!!
    },
)


###
### Verify access token 
###
def jwt_decode_no_verification(token):
    parts = token.split('.')
    if len(parts) != 3:
        raise Exception("Token no te 3 parts!")

    payload = parts[1]
    # si hay padding fes:
    if len(payload) % 4 != 0:
        payload += '=' * (-len(payload) % 4)

    decoded_bytes = base64.urlsafe_b64decode(payload)
    claims = json.loads(decoded_bytes)
    return claims

def require_valid_token(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        access_token = session.get("access_token")
        if not access_token:
            flash("Acces denegat: token no present.", "danger")
            app.logger.error("Acces denegat token no present")
            return redirect("/logout")
        try:
            # decode token sin verificar firma para extraer los claims
            decoded = jwt_decode_no_verification(access_token)
        except Exception as e:
            app.logger.error(f"Acces denegat token invalid: {e}")
            flash("Acces denegat: token invalid.", "danger")
            return redirect("/logout")        
        
        # verificar dades critiques
        app.logger.debug(f"decoded jwt: {decoded}")
        user_session = session.get("user", {})
        token_email = decoded.get("sub")
        token_eid = decoded.get("eid")
        token_issuer = decoded.get("iss")

        # verificar patro eid (employeeNumber)
        pattern = r'^\d{4}[A-Z]$'
        if (not re.fullmatch(pattern, token_eid)):
            app.logger.error(f"Eid: {token_eid} incorrecte!")
            flash("Employee Number incorrecte!", "danger")
            return redirect("/logout")

        if token_email != user_session["email"] or token_eid != user_session["eid"] or token_issuer != OKTA_DOMAIN:
            app.logger.error(f"Dades d'usuari inconsistents!!!")
            flash("Dades d'usuari inconsistents, si us plau inicia sesio de nou.", "danger")
            return redirect("/logout")        

        return f(*args, **kwargs)
    return decorated_function

###
### Api calls methods
###
# auth http headers for okta api 
headers = {
    "Authorization": f"SSWS {API_TOKEN}",
    "Content-Type": "application/json"
}

# find id with email
def get_okta_user_id(email):
    response = requests.get(f"{OKTA_ORG_URL}/api/v1/users/{email}", headers=headers)
    if response.status_code == 200:
        id_user = response.json()["id"]
        app.logger.debug(f"Id de l'usuari: {id_user}")
        return id_user
    else:
        app.logger.error(f"Error obtenint usuari d'Okta: {response.text}")
        return None

# modif profile in Okta
def update_okta_user_profile(user_id, profile_data):
    data = {
        "profile": profile_data
    }
    app.logger.debug(f"Update profile okta: {data}")
    response = requests.post(f"{OKTA_ORG_URL}/api/v1/users/{user_id}", headers=headers, json=data)
    if response.status_code == 200:
        app.logger.info(f"Perfil d'Okta actualitzat correctament: {profile_data}")
        return True
    else:
        app.logger.error(f"Error actualitzant perfil d'usuari a Okta: {response.text}")
        return False

# change password in Okta
def change_okta_user_password(user_id, curr_psswd, new_psswd):
    # NO son segurs mai mostrar pwd en text pla
    app.logger.debug(f"pwd:{curr_psswd}")
    app.logger.debug(f"newpwd:{new_psswd}")
    data = {
        "oldPassword": {"value": curr_psswd},
        "newPassword": {"value": new_psswd}
    }
    url = f"{OKTA_ORG_URL}/api/v1/users/{user_id}/credentials/change_password"
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        app.logger.info("Contrasenya actualitzada a Okta")
        return True
    else:
        app.logger.error(f"Error actualitzant contrasenya a Okta: {response.text}")
        return False

### ENTRA ID api calls
# get token to use graph api
def get_graph_token():
    url = f"{ENTRAID_AUTHORITY}/oauth2/v2.0/token"
    payload = {
        "grant_type": "client_credentials",
        "client_id": ENTRAID_CLIENT_ID,
        "client_secret": ENTRAID_CLIENT_SECRET,
        "scope": f"{GRAPH_URL}/.default"
    }
    response = requests.post(url, data=payload)
    response.raise_for_status()
    token = response.json().get("access_token")
    if not token:
        app.logger.error(f"Access token no obtingut: {response.text}")
        raise RuntimeError(f"Access token no obtingut: {response.text}")
    return token

# update user in Entra ID
def update_entraid_user_profile(userPrincipalName, displayName):
    data = {
        "displayName": displayName
    }
    headers_entraid = {
        "Authorization": f"Bearer {get_graph_token()}",
        "Content-Type": "application/json"
    }
    app.logger.debug(f"Update Entra ID user: {userPrincipalName}, {displayName}")
    response = requests.patch(f"{GRAPH_URL}/v1.0/users/{userPrincipalName}", headers=headers_entraid, json=data)
    if response.status_code in (200, 204): # then its ok
        app.logger.info(f"Perfil Entra ID actualitzar correctament: {data}")
        return True
    else:
        app.logger.error(f"Error actualitzant perfil a Entra ID: {response.text}")
        return False

# change password in Entra id
def change_entraid_user_password(userPrincipalName, curr_psswd, new_psswd):
    # NO son segurs mai mostrar pwd en text pla 
    app.logger.debug(f"entraid pwd:{curr_psswd}")
    app.logger.debug(f"entraid newpwd:{new_psswd}")
    data = {
        "currentPassword": curr_psswd,
        "newPassword": new_psswd
    }
    headers_entraid = {
        "Authorization": f"Bearer {get_graph_token()}",
        "Content-Type": "application/json"
    }
    url = f"{GRAPH_URL}/v1.0/users/{userPrincipalName}/changePassword"
    response = requests.post(url, headers=headers_entraid, json=data)
    if response.status_code in (200, 204): # then its ok
        app.logger.info(f"Contrasenya actualitzada a Entra ID")
        return True
    else:
        app.logger.error(f"Error actualitzant contrasenya a Entra ID: {response.text}")
        return False

### 
### ENDPOINTS
###
# / endpoint
@app.route("/")
def home():
    provider = session.get("provider")
    if provider == "okta":
        user = session.get("user")
        if user:
            app.logger.info(f"Usuari autenticat {user}")
            return render_template("home.html", user=user)
        else:
            app.logger.info("Usuari no autenticat.")
            return render_template("home.html", user=user)
    elif provider == "entra_id":
        user = session.get("entraid_user")
        if user:
            app.logger.info(f"Usuari autenticat {user}")
            return render_template("home.html", user=user)
        else:
            app.logger.info("Usuari no autenticat.")
            return render_template("home.html", user=user)
    else:
        app.logger.info("Usuari no autenticat")
        return render_template("home.html", user=None)


# /login endpoint for Okta
@app.route("/login")
def login():
    redirect_uri = url_for("auth", _external=True)
    nonce = os.urandom(16).hex()
    app.logger.debug(f"Asignem nonce a la sessio actual: {nonce}")
    session["nonce"] = nonce
    app.logger.info(f"Redireccionem a uri: {redirect_uri}")
    return okta_oauth.authorize_redirect(redirect_uri, nonce=nonce)

# /login endpoint for Okta
@app.route("/login_entraid")
def login_entraid():
    nonce = os.urandom(16).hex()
    app.logger.debug(f"Asignem nonce a la sessio actual: {nonce}")
    session["nonce"] = nonce
    redirect_uri = url_for("auth_entraid", _external=True)
    app.logger.info(f"Redireccionem a uri: {redirect_uri}")
    return entraid_oauth.authorize_redirect(redirect_uri, nonce=nonce)

# /auth/callback redirect after login OKTA
@app.route("/auth/callback")
def auth():
    # 73-83 TODO: check
    token = okta_oauth.authorize_access_token()
    app.logger.debug(f"Token obtingut: {token}")
    nonce = session.pop("nonce", None)  
    if not nonce:
        app.logger.error("Nonce no trobat en la sessio!")
        return "Error: Nonce perdut o no valid", 400
    user_info = okta_oauth.parse_id_token(token, nonce)
    app.logger.debug(f"User parsed token {user_info}")
    session["provider"] = "okta"
    session["id_token"] = token.get("id_token")
    session["access_token"] = token.get("access_token")
    session["user"] = {
        "name": user_info["name"],
        "email": user_info["email"],
        "eid": user_info["eid"]
    }
    app.logger.info(f"Sessio info usuari: {user_info["name"]}, email: {user_info["email"]}, eid: {user_info["eid"]}")

    # guardar user si no exist en db
    existing_user = User.query.filter_by(email=user_info["email"]).first()
    if not existing_user:
        app.logger.debug(f"User {user_info["name"]} no guardat en db")
        new_user = User(
            email=user_info["email"],
            full_name=user_info["name"],
            eid=user_info["eid"]
        )
        db.session.add(new_user)
        db.session.commit()
        app.logger.debug(f"User {user_info["name"]} guardat en db")
    else:
        app.logger.debug(f"User trobat in db: {existing_user.email}")

    return redirect("/")

# /getAToken redirect after login ENTRA ID
@app.route("/auth/entraid/callback")
def auth_entraid():
    token = entraid_oauth.authorize_access_token()
    app.logger.debug(f"Token obtingut: {token}")
    nonce = session.pop("nonce", None)  
    if not nonce:
        app.logger.error("Nonce no trobat en la sessio!")
        return "Error: Nonce perdut o no valid", 400
    user_info = entraid_oauth.parse_id_token(token, nonce)
    app.logger.debug(f"User parsed token {user_info}")
    session["provider"] = "entra_id"
    session["entraid_id_token"] = token.get("id_token"),
    session["entraid_access_token"] = token.get("access_token"),
    session["entraid_user"] = {
            "name": user_info["name"],
            "email": user_info["preferred_username"], 
            "eid":   user_info["eid"]
    }
    
    app.logger.info(f"Sessio info usuari: {session["entraid_user"]["name"]}, email: {session["entraid_user"]["email"]}, eid: {session["entraid_user"]["eid"]}") 
    
    existing_user = User.query.filter_by(email=session["entraid_user"]["email"]).first()
    if not existing_user:
        app.logger.debug(f"User {user_info["name"]} no guardat en db")
        new_user = User(
            email= session["entraid_user"]["email"], 
            full_name = user_info["name"],
            eid = user_info["eid"]
        )
        db.session.add(new_user)
        db.session.commit()
        app.logger.debug(f"User {user_info["name"]} guardat en db")
    else:
        app.logger.debug(f"User trobat in db: {existing_user.email}")
    return redirect("/")

# /profile endpoint per veure i editar el perfil
@app.route("/profile")
@require_valid_token
def profile():
    user = session.get("user")
    if not user:
        app.logger.warning("Usuari perdut al intentar modificar perfil!")
        return redirect("/login")
    
    db_user = User.query.filter_by(email=user["email"]).first()
    app.logger.info(f"User a modifcar: {db_user}")
    return render_template("profile.html", user=db_user)

# /update_profile per modificar el perfil
@app.route("/update_profile", methods=["POST"])
@require_valid_token
def update_profile():
    user = session.get("user")
    app.logger.info(f"upduser user:{user}")
    if not user:
        return redirect("/login")
    
    # dades del formulari (full_name)
    full_name = request.form.get("full_name")
    app.logger.info(f"NEW full_name: {full_name}")
    app.logger.info(f"email: {user["email"]}")
    
    # si no modifica full_name torna a profile
    if not full_name:
        return redirect("/profile")
    
    # obtenir usuari actual de la db
    current_user = User.query.filter_by(email=user["email"]).first()
    if not current_user:
        flash("Usuari no trobat", "danger")
        return redirect('/profile')
    
    try:
        # actualitzar usuari a Okta
        okta_user_id = get_okta_user_id(user["email"])
        if okta_user_id:
            profile_data = {
                "firstName": full_name.split()[0],
                "lastName": ' '.join(full_name.split()[1:]) if len(full_name.split()) > 1 else "",
                "email": user["email"],
                "login": user["email"],
                "displayName": full_name,
                "employeeNumber": user["eid"]
            }
            if update_okta_user_profile(okta_user_id, profile_data):
                # si actualitzacio a Okta exit, actualitzar la BD 
                current_user.full_name = full_name
                db.session.commit()
                
                # actualitzar la sessio
                session["user"] = {
                    "name": full_name,
                    "email": user["email"],
                    "eid": user["eid"]
                }
                
                flash("Perfil actualitzat correctament", "success")
            else:
                flash("Error en actualitzar el perfil a Okta", "danger")
        else:
            flash("No s'ha pogut trobar l'usuari a Okta", "danger")
    except Exception as e:
        db.session.rollback()
        app.logger.error(f"Error en actualitzar el perfil: {str(e)}")
        flash(f"Error en actualitzar el perfil: {str(e)}", "danger")
    
    return redirect("/profile")

# /password endpoint to show change password view
@app.route("/password")
def password():
    return render_template("change_password.html")

# /change_password call Okta api to change psswd
@app.route("/change_password", methods=["POST"])
@require_valid_token
def change_password():
    user = session.get("user")
    app.logger.info(f"chpwd user:{user}")
    if not user:
        return redirect("/login")
    
    curr_psswd = request.form.get("curr_psswd")
    new_psswd = request.form.get("new_psswd")
    confirm_new_psswd = request.form.get("confirm_new_psswd")

    if not curr_psswd or not new_psswd or not confirm_new_psswd:
        flash("Tots els camps son obligatoris!", "danger")
        return redirect("/password")

    if new_psswd != confirm_new_psswd:
        flash("Les contrasenyes no coincideixen!", "danger")
        return redirect("/passowrd")

    okta_user_id = get_okta_user_id(user["email"])
    if not okta_user_id:
        flash("No s'ha pogut trobar el id de l'usuari a Okta", "danger")
        return redirect("/password")
    
    if change_okta_user_password(okta_user_id, curr_psswd, new_psswd):
        flash("Contrasenya actualitzada correctament", "success")
    else:
        flash("Error a l'actualitzar contrasenya! Proba una mes segura!", "danger")
    
    # tornem al profile view
    return redirect("/profile")


# /logout endpoint
@app.route("/logout")
def logout():
    # get prov
    provider = session.get("provider")

    if provider == "entra_id":
        id_token = session.pop("entraid_id_token", None)
    else: # okta
        id_token = session.pop("id_token", None)

    app.logger.debug(f"Token de la sessio: {id_token}")

    if provider == "entra_id":
        logout_url = f"{ENTRAID_AUTHORITY}/oauth2/v2.0/logout?post_logout_redirect_uri={url_for("home", _external=True)}"
        if id_token:
            logout_url += f"&id_token_hint={id_token}"
    else: # okta
        logout_url = f"{OKTA_DOMAIN}/v1/logout?post_logout_redirect_uri={url_for("home", _external=True)}"
        if id_token:
            logout_url += f"&id_token_hint={id_token}"

    session.clear()

    app.logger.debug(f"Logout url de {provider}: {logout_url}")
    return redirect(logout_url)


###
### MAIN
###
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, ssl_context=("/home/pablofc18/myApp/APPWITHFLASK/certs/cert.pem",
                                                    "/home/pablofc18/myApp/APPWITHFLASK/certs/key.pem"))