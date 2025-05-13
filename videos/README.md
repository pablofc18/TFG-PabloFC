# Carpeta `videos`

Aquest directori conté diversos vídeos demostratius i les seves captures associades.

---

## `flask-jenkins-PFC-OKTA_chname.mp4`

- **Explicació:**  
  En aquest vídeo es mostra el funcionament del SSO (Single Sign-On), s'inicia sessió amb Okta amb l'usuari **pablo.franco.c@estudiantat.upc.edu** en l'app de Flask i es modifica el nom del perfil, que s'actualitza tant a Okta com a la base de dades (captura associada). I després, s'inicia sessió a Jenkins comprovant que no cal introduir credencials gràcies al SSO. Per últim, es tanca sessió.
- **Fitxer de captura associat:** [`chname-PFC-OKTA.jpg`](https://github.com/pablofc18/myApp/blob/master/videos/chname-PFC-OKTA.jpg)
- **Comentaris sobre la captura:**  
  En la captura es pot observar els logs tant de l'app de Flask com de les connexions amb Okta. On es pot veure la informació de l'usuari abans i després de fer el canvi de nom (s'elimina l'últim cognom).

> Cal destacar que el codi de MFA que s'escriu en aquest vídeo s'obté de l'aplicació mòvil **Okta Verify**.

---

## `flask-jenkins-user9-OKTA_chpwd.mp4`

- **Explicació:**  
  En aquest vídeo es mostra el funcionament del SSO (Single Sign-On) també, s'inicia sessió amb Okta amb l'usuari **user9 user9** en l'app de Flask i es modifica la contrasenya, que s'actualitza a Okta. I després, s'inicia sessió a Jenkins comprovant que l'usuari no té l'aplicació asignada, el seu grup no pot accedir al servei de Jenkins. Per últim, es tanca sessió.
- **Fitxer de captura associat:** [`chpwd-user9-OKTA.jpg`](https://github.com/pablofc18/myApp/blob/master/videos/chpwd-user9-OKTA.jpg)
- **Comentaris sobre la captura:**  
  En la captura es pot observar els logs tant de l'app de Flask com de les connexions amb Okta. On es pot veure la contrasenya antiga i la nova (en un entorn real no s'hauria de mostrar).

> Cal destacar que el codi de MFA que s'escriu tant en aquest vídeo com l'anterior s'obté de l'aplicació mòvil **Okta Verify**.

---

## `jenkins-loginOkta.mp4`

- **Explicació:**  
  En aquest vídeo es mostra el login amb Okta amb l'usuari **pablo.franco.c@estudiantat.upc.edu** (que si té accés) des del servei de Jenkins, ja que en els anteriors dos vídeos no es pot observar com et redirecciona a Okta.

> Cal destacar que el codi de MFA que s'escriu tant en aquest vídeo com els anteriors s'obté de l'aplicació mòvil **Okta Verify**.

---

## `connectors-EntraID-u-g.mp4`

- **Explicació:**  
  En aquest vídeo es mostra
