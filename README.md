# Repositori de material suplementari. TFG-PabloFC 

Aquest repositori conté el codi de la app Flask en les diferents fases de la migració i el material suplementari.

- Para leer explicación en español click aquí: [ESP](https://github.com/pablofc18/myApp/blob/master/README.es.md)

---

## Estructura de la branca `master`

En la branca `master` trobaràs:

- **`connectors/`**  
  - Carpeta amb scripts i classes auxiliars per dur a terme la migració de dades.  
  - **`connectors/response_files/`**   
    - Carpeta on es troben els diferents fitxers xifrats extrets dels scripts dels connectors. (Excepte els dos BATCH_* que no estan xifrats).
- **`jenkins_pipelines/`**  
  - Carpeta on es troben els dos pipelines de Jenkins per desplegar i aturar l'aplicació de Flask de la VM1.
- **`videos/`**  
  - Carpeta amb vídeos demostratius.  
  - Cada vídeo està documentat amb un petit README.

> Aquesta branca serveix de punt de partida i conté els connectors, els pipelines de Jenkins i els vídeos demostratius.
---

## Branca `okta`

Conté la versió de l’aplicació Flask **integrada amb Okta** com a sistema d’autenticació.

- **`APPWITHFLASK/`** – Carpeta on es troba el codi l'aplicació web Flask i la resta d'arxius necessaris.
- **`APPWITHFLASK/app.py`** – Fitxer amb el codi l'aplicació web Flask, click [aquí](https://github.com/pablofc18/myApp/blob/okta/APPWITHFLASK/app.py) per veure'l.

> Click [aquí](https://github.com/pablofc18/myApp/tree/okta) per anar a la branca.
---

## Branca `dual_run`

Aquesta branca implementa la **fase de dual-run**, on l’aplicació suporta simultàniament: **Okta** i **Microsoft Entra ID**.

- **`APPWITHFLASK/`** – Carpeta on es troba el codi l'aplicació web Flask i la resta d'arxius necessaris.
- **`APPWITHFLASK/app.py`** – Fitxer amb el codi l'aplicació web Flask, click [aquí](https://github.com/pablofc18/myApp/blob/okta/APPWITHFLASK/app.py) per veure'l.

> Click [aquí](https://github.com/pablofc18/myApp/tree/dual_run) per anar a la branca.
---

## Branca `entraid`

Conté la versió finalitzada la migració de l’aplicació **integrada amb Microsoft Entra ID**.

- **`APPWITHFLASK/`** – Carpeta on es troba el codi l'aplicació web Flask i la resta d'arxius necessaris.
- **`APPWITHFLASK/app.py`** – Fitxer amb el codi l'aplicació web Flask, click [aquí](https://github.com/pablofc18/myApp/blob/okta/APPWITHFLASK/app.py) per veure'l.

> Click [aquí](https://github.com/pablofc18/myApp/tree/entraid) per anar a la branca.

---

> Es destaca que apareixen secrets al fitxers de logs i arxius que NO haurien d'estar en un projecte estàndard, en aquest cas tot el que es pot observar es mostra de manera intencionada a efectes demostratius i no té cap afectació al projecte.



