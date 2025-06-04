# Videos Microsoft Entra ID 

### [`1.0.EntraID-flask-jenkins-user1-chname.mp4`](https://github.com/pablofc18/myApp/blob/master/videos/3.EntraID/1.0.EntraID-flask-jenkins-user1-chname.mp4)

- **Explicació:**  
  En aquest vídeo es mostra el funcionament del SSO (Single Sign-On), s'inicia sessió amb EntraID amb l'usuari **user1 user1** en l'app de Flask i es modifica el nom del perfil, que s'actualitza tant a Entra ID com a la base de dades. I després, s'inicia sessió a Jenkins comprovant que no cal introduir credencials gràcies al SSO. Per últim, es tanca sessió.
- **Fitxers de captures associades:** [`1.1.EntraID-chname-user1.jpg`](https://github.com/pablofc18/myApp/blob/master/videos/3.EntraID/1.1.EntraID-chname-user1.jpg) [`1.2.EntraID-chname-user1-WebLog.jpg`](https://github.com/pablofc18/myApp/blob/master/videos/3.EntraID/1.2.EntraID-chname-user1-WebLog.jpg) 
- **Comentaris sobre la captura:**  
  En les captures es pot observar els logs tant de l'app de Flask com de la web d'Entra ID. On es pot veure la informació de l'usuari abans i després de fer el canvi de nom.
  > Es destaca que els logs de l'app de Flask tenen 2 hores endarrerides de diferencia!

> Cal destacar que el codi de MFA que s'escriu en aquest vídeo s'obté de l'aplicació mòvil **EntraID Verify**.

---

### [`2.0.EntraID-flask-jenkins-user9-chpwd.mp4`](https://github.com/pablofc18/myApp/blob/master/videos/3.EntraID/2.0.EntraID-flask-jenkins-user9-chpwd.mp4)

- **Explicació:**  
  En aquest vídeo es mostra el funcionament del SSO (Single Sign-On) també, s'inicia sessió amb EntraID amb l'usuari **user9 user9** en l'app de Flask i es modifica la contrasenya, que s'actualitza a EntraID. I després, s'inicia sessió a Jenkins comprovant que l'usuari no té l'aplicació asignada, el seu grup no pot accedir al servei de Jenkins. Per últim, es tanca sessió.
- **Fitxers de captures associades:** [`2.1.EntraID-chpwd-user9.jpg`](https://github.com/pablofc18/myApp/blob/master/videos/3.EntraID/2.1.EntraID-chpwd-user9.jpg) [`2.2.EntraID-chpwd-user9-WebLog.jpg`](https://github.com/pablofc18/myApp/blob/master/videos/3.EntraID/2.2.EntraID-chpwd-user9-WebLog.jpg)
- **Comentaris sobre la captura:**  
  En les captures es pot observar els logs tant de l'app de Flask com de la web d'EntraID. On es pot veure la contrasenya antiga i la nova (en un entorn real no s'hauria de mostrar) i el ChangePassword al log de la web d'Entra ID.
  > Es destaca que els logs de l'app de Flask tenen 2 hores endarrerides de diferencia!

> Cal destacar que el codi de MFA que s'escriu tant en aquest vídeo com l'anterior s'obté de l'aplicació mòvil **EntraID Verify**.

---

### [`3.0.EntraID-jenkins-login.mp4`](https://github.com/pablofc18/myApp/blob/master/videos/3.EntraID/3.0.EntraID-jenkins-login.mp4)

- **Explicació:**  
  En aquest vídeo es mostra el login amb EntraID amb l'usuari **Pablo Franco** (que si té accés) des del servei de Jenkins, ja que en els anteriors dos vídeos no es pot observar com et redirecciona a EntraID.

> Cal destacar que el codi de MFA que s'escriu tant en aquest vídeo com els anteriors s'obté de l'aplicació mòvil **EntraID Verify**.
