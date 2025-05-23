# Video Dual_run

### [`dualrun-changeName.mp4`](https://github.com/pablofc18/myApp/blob/master/videos/Dual_run/dualrun-changeName.mp4)

- **Explicació:**  
  En aquest vídeo es mostra el funcionament de l'aplicació Flask integrada amb Okta i Entra ID al mateix temps. Primer s'inicia sessió amb l'usuari **user9 user9** amb Microsoft Entra ID (fent ús del MFA), es canvia el nom de l'usuari i es tanca sessió. Després, s'inicia un altre cop sessió però amb Okta (també fent ús de MFA), on es pot veure el nou nom de l'usuari que acabem de modificar a **user9 user9 dualrun**, i per últim es torna a canviar el nom al que tenia abans i es tanca sessió. 
- **Fitxers de captura associats:** 1.[`dualrun-logEntraID-chname.jpg`](https://github.com/pablofc18/myApp/blob/master/videos/Dual_run/dualrun-logEntraID-chname.jpg) 2.[`dualrun-logEntraID-chname-02.jpg`](https://github.com/pablofc18/myApp/blob/master/videos/Dual_run/dualrun-logEntraID-chname-02.jpg) 3.[`dualrun-logOkta-chname.jpg`](https://github.com/pablofc18/myApp/blob/master/videos/Dual_run/dualrun-logOkta-chname.jpg)
- **Comentaris sobre la captura:**  
  1. A la primera captura, s'observen els logs extrets d'Entra ID, on indica els dos "Update user" que hi ha hagut amb l'usuari **user9 user9** des de l'aplicació **myAppFlask**. 
  2. A la segona captura, que complimenta la primera, es pot veure un dels dos logs anteriors els camps que s'han modificat de l'usuari, el **displayName**.
  3. A la tercera captura, s'observen dos dels logs extrets a Okta, on indica l'"Update user" que hi ha hagut amb l'usuari **user9 user9**.

> Cal destacar que els codi de MFA que s'escriuen en aquest vídeo s'obté de l'aplicació mòvil **Okta Verify** i **Microsoft Authenticator**.
