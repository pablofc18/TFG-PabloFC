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
        logging.FileHandler("log/flaskApp.log"),
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


app.config["SESSION_COOKIE_NAME"] = "login-session"
app.config["SESSION_PERMANENT"] = False # user session terminara si es tanca navegador 

# conf entra id
ENTRAID_TENANT_ID     = os.getenv("ENTRAID_TENANT_ID")
ENTRAID_CLIENT_ID     = os.getenv("ENTRAID_CLIENT_ID")
ENTRAID_CLIENT_SECRET = os.getenv("ENTRAID_CLIENT_SECRET")
ENTRAID_AUTHORITY     = f"{os.getenv("LOGIN_MICROSOFT_URL")}/{ENTRAID_TENANT_ID}"
ENTRAID_OPENID_CONFIG = f"{ENTRAID_AUTHORITY}/v2.0/.well-known/openid-configuration"
GRAPH_URL             = os.getenv("GRAPH_URL")

# conf oauth Entra id
oauth = OAuth(app)
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
        access_token = session.get("entraid_access_token")
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
        
        app.logger.debug(f"decoded ENTRA ID jwt: {decoded}")
        user_session = session.get("entraid_user", {})
        token_email = decoded.get("preferred_username")
        token_eid = decoded.get("eid")
        token_issuer = decoded.get("iss")

        # verificar pattern eid (employeeNumber)
        pattern = r'^\d{4}[A-Z]$'
        if (not re.fullmatch(pattern, token_eid)):
            app.logger.error(f"Eid: {token_eid} incorrecte!")
            flash("Employee Number incorrecte!", "danger")
            return redirect("/logout")

        if token_email != user_session["email"] or token_eid != user_session["eid"] or token_issuer != f"{ENTRAID_AUTHORITY}/v2.0":
            app.logger.error(f"Dades d'usuari inconsistents!!!")
            flash("Dades d'usuari ENTRAID inconsistents, si us plau inicia sesio de nou.", "danger")
            return redirect("/logout")        

        return f(*args, **kwargs)
    return decorated_function

###
### Api calls methods
###

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

# find user by eid
def find_entraid_user_by_eid(eid):
    url = f"{GRAPH_URL}/v1.0/users"
    parameters = {
        "$filter": f"employeeID eq '{eid}'"
    }
    headers_entraid = {
        "Authorization": f"Bearer {get_graph_token()}",
        "Content-Type": "application/json"
    }
    response = requests.get(url, headers=headers_entraid, params=parameters)
    response.raise_for_status()
    id_user = response.json()["value"][0]["id"]
    app.logger.debug(f"Id de l'usuari: {id_user}")
    return id_user if id_user else None
    

### 
### ENDPOINTS
###
# / endpoint
@app.route("/")
def home():
    user = session.get("entraid_user")
    if user:
        app.logger.info(f"Usuari autenticat {user}")
        return render_template("home.html", user=user)
    else:
        app.logger.info("Usuari no autenticat.")
        return render_template("home.html", user=user)

# /login endpoint for Okta
@app.route("/login_entraid")
def login_entraid():
    nonce = os.urandom(16).hex()
    app.logger.debug(f"Asignem nonce a la sessio actual: {nonce}")
    session["nonce"] = nonce
    redirect_uri = url_for("auth_entraid", _external=True)
    app.logger.info(f"Redireccionem a uri: {redirect_uri}")
    return entraid_oauth.authorize_redirect(redirect_uri, nonce=nonce)

# /auth/entraid/callback redirect after login ENTRA ID
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
    session["entraid_access_token"] = token.get("access_token")
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
            email= user_info["email"], 
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
    user = session.get("entraid_user")
    if not user:
        app.logger.warning("Usuari perdut al intentar modificar perfil!")
        return redirect("/login_entraid")
    
    db_user = User.query.filter_by(email=user["email"]).first()
    app.logger.info(f"User a modifcar: {db_user}")
    return render_template("profile.html", user=db_user)

# /update_profile per modificar el perfil
@app.route("/update_profile", methods=["POST"])
@require_valid_token
def update_profile():
    user = session.get("entraid_user")
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
    
    # obtenir usuaris de la db amb mateix eid
    curr_users = User.query.filter_by(eid=user["eid"]).all()
    if not curr_users:
        flash("Cap usuari trobat!", "danger")
        return redirect('/profile')
    
    try:
        # actualitzar usuari a Entra id
        userPrincipalName = find_entraid_user_by_eid(user["eid"])
        if not userPrincipalName:
            flash("No s'ha pogut trobar l'usuari a EntraID", "danger")
        if update_entraid_user_profile(userPrincipalName, full_name):
            for u in curr_users: # estara l'usuari d'okta en la db encara
                u.full_name = full_name
            db.session.commit()
            # actualitzar la sessio 
            session["entraid_user"] = {
                "name": full_name,
                "email": user["email"],
                "eid": user["eid"]
            }
            flash("Perfil actualitzat correctament a EntraID", "success")
        else:
            flash("Error en actualitzar el perfil a EntraID", "danger")
    except Exception as e:
        db.session.rollback()
        app.logger.error(f"Error en actualitzar el perfil a EntraID: {str(e)}")
        flash(f"Error en actualitzar el perfil a EntraID: {str(e)}", "danger")
    
    return redirect("/profile")

# /password endpoint to show change password view
@app.route("/password")
def password():
    return render_template("change_password.html")

# /change_password call Okta api to change psswd
@app.route("/change_password", methods=["POST"])
@require_valid_token
def change_password():
    user = session.get("entraid_user")
    app.logger.info(f"chpwd user:{user}")
    if not user:
        return redirect("/login_entraid")
    
    curr_psswd = request.form.get("curr_psswd")
    new_psswd = request.form.get("new_psswd")
    confirm_new_psswd = request.form.get("confirm_new_psswd")

    if not curr_psswd or not new_psswd or not confirm_new_psswd:
        flash("Tots els camps son obligatoris!", "danger")
        return redirect("/password")

    if new_psswd != confirm_new_psswd:
        flash("Les contrasenyes no coincideixen!", "danger")
        return redirect("/passowrd")

    userPrincipalName = find_entraid_user_by_eid(user["eid"])
    if not userPrincipalName:
        flash("No s'ha pogut trobar l'usuari a EntraID", "danger")

    if change_entraid_user_password(userPrincipalName, curr_psswd, new_psswd):
        flash("Contrasenya actualitzada correctament a Entra ID", "success")
    else:
        flash("Error a l'actualitzar contrasenya a EntraID!", "danger")
    
    # tornem al profile view
    return redirect("/profile")


# /logout endpoint
@app.route("/logout")
def logout():
    id_token = session.pop("entraid_id_token", None)

    app.logger.debug(f"Token de la sessio: {id_token}")

    logout_url = f"{ENTRAID_AUTHORITY}/oauth2/v2.0/logout?post_logout_redirect_uri={url_for("home", _external=True)}"
    if id_token:
        logout_url += f"&id_token_hint={id_token}"

    session.clear()

    app.logger.debug(f"Logout url d'Entra ID: {logout_url}")
    return redirect(logout_url)


###
### MAIN
###
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, ssl_context=("/home/pablofc18/myApp/APPWITHFLASK/certs/cert.pem",
                                                    "/home/pablofc18/myApp/APPWITHFLASK/certs/key.pem"))