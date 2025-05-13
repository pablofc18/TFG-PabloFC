# Repositori TFG PabloFC 

Aquest repositori conté el codi de la app Flask en les diferents fases de la migració i el material suplementari (videos, connectors)

---

## Estructura de la branca `master`

En la branca `master` trobaràs:

- **`connectors/`**  
  Carpeta amb scripts i classes auxiliars per dur a terme la migració de dades.  
  - **`connectors/response_files/`**   
    Carpeta on es troben els diferents fitxers xifrats extrets dels scripts dels connectors. (Excepte BATCH_* que es pot veure).
- **`videos/`**  
  Carpeta amb vídeos demostratius.  
  - Cada vídeo està documentat amb un petit README.

> Aquesta branca serveix de punt de partida i conté només els connectors i els vídeos.

---

## Branca `okta`

Conté la versió de l’aplicació Flask **integrada amb Okta** com a sistema d’autenticació.

- **`APPWITHFLASK/`** – Carpeta on es troba el codi l'aplicació web Flask i la resta d'arxius necessaris.
- **`APPWITHFLASK/app.py`** – Fitxer amb el codi l'aplicació web Flask, clicka [aquí](https://github.com/pablofc18/myApp/blob/okta/APPWITHFLASK/app.py) per veure'l. .

---

## Branca `dual_run`

Aquesta branca implementa la **fase de dual-run**, on l’aplicació suporta simultàniament: **Okta** i **Microsoft Entra ID**.

- **`APPWITHFLASK/`** – Carpeta on es troba el codi l'aplicació web Flask i la resta d'arxius necessaris.
- **`APPWITHFLASK/app.py`** – Fitxer amb el codi l'aplicació web Flask, clicka [aquí](https://github.com/pablofc18/myApp/blob/okta/APPWITHFLASK/app.py) per veure'l. .

---

## Branca `entraid`

Conté la versió finalitzada la migració de l’aplicació **integrada amb Microsoft Entra ID**.

- **`APPWITHFLASK/`** – Carpeta on es troba el codi l'aplicació web Flask i la resta d'arxius necessaris.
- **`APPWITHFLASK/app.py`** – Fitxer amb el codi l'aplicació web Flask, clicka [aquí](https://github.com/pablofc18/myApp/blob/okta/APPWITHFLASK/app.py) per veure'l. .

---
