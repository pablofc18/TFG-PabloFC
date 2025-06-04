# Videos Okta

### [`1.0.Okta-flask-jenkins-PFC-chname.mp4`](https://github.com/pablofc18/myApp/blob/master/videos/1.Okta/1.0.Okta-flask-jenkins-PFC-chname.mp4)

- **Explicació:**  
  En aquest vídeo es mostra el funcionament del SSO (Single Sign-On), s'inicia sessió amb Okta amb l'usuari **Pablo Franco Carrasco** en l'app de Flask i es modifica el nom del perfil, que s'actualitza tant a Okta com a la base de dades (captura associada). I després, s'inicia sessió a Jenkins comprovant que no cal introduir credencials gràcies al SSO. Per últim, es tanca sessió.
- **Fitxer de captura associat:** [`1.1.Okta-chname-PFC.jpg`](https://github.com/pablofc18/myApp/blob/master/videos/1.Okta/1.1.Okta-chname-PFC.jpg)
- **Comentaris sobre la captura:**  
  En la captura es pot observar els logs tant de l'app de Flask com de les connexions amb Okta. On es pot veure la informació de l'usuari abans i després de fer el canvi de nom (s'elimina l'últim cognom).
  > Es destaca que els logs de l'app de Flask tenen 2 hores endarrerides de diferencia!

> Cal destacar que el codi de MFA que s'escriu en aquest vídeo s'obté de l'aplicació mòvil **Okta Verify**.

---

### [`2.0.Okta-flask-jenkins-user9-chpwd.mp4`](https://github.com/pablofc18/myApp/blob/master/videos/1.Okta/2.0.Okta-flask-jenkins-user9-chpwd.mp4)

- **Explicació:**  
  En aquest vídeo es mostra el funcionament del SSO (Single Sign-On) també, s'inicia sessió amb Okta amb l'usuari **user9 user9** en l'app de Flask i es modifica la contrasenya, que s'actualitza a Okta. I després, s'inicia sessió a Jenkins comprovant que l'usuari no té l'aplicació asignada, el seu grup no pot accedir al servei de Jenkins. Per últim, es tanca sessió.
- **Fitxer de captura associat:** [`2.1.Okta-chpwd-user9.jpg`](https://github.com/pablofc18/myApp/blob/master/videos/1.Okta/2.1.Okta-chpwd-user9.jpg)
- **Comentaris sobre la captura:**  
  En la captura es pot observar els logs tant de l'app de Flask com de les connexions amb Okta. On es pot veure la contrasenya antiga i la nova (en un entorn real no s'hauria de mostrar).
  > Es destaca que els logs de l'app de Flask tenen 2 hores endarrerides de diferencia!

> Cal destacar que el codi de MFA que s'escriu tant en aquest vídeo com l'anterior s'obté de l'aplicació mòvil **Okta Verify**.

---

### [`3.0.Okta-jenkins-login.mp4`](https://github.com/pablofc18/myApp/blob/master/videos/1.Okta/3.0.Okta-jenkins-login.mp4)

- **Explicació:**  
  En aquest vídeo es mostra el login amb Okta amb l'usuari **Pablo Franco Carrasco** (que si té accés) des del servei de Jenkins, ja que en els anteriors dos vídeos no es pot observar com et redirecciona a Okta.

> Cal destacar que el codi de MFA que s'escriu tant en aquest vídeo com els anteriors s'obté de l'aplicació mòvil **Okta Verify**.
