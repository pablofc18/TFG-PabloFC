# Repositorio de material suplementario. TFG-PabloFC

Este repositorio contiene el código de la app Flask en las diferentes fases de la migración y el material suplementario.

---
## Estructura de la rama `master`
En la rama `master` encontrarás:
- **`connectors/`**  
  - Carpeta con scripts y clases auxiliares para llevar a cabo la migración de datos.  
  - **`connectors/response_files/`**   
    - Carpeta donde se encuentran los diferentes archivos cifrados extraídos de los scripts de los conectores. (Excepto los dos BATCH_* que no están cifrados).
- **`jenkins_pipelines/`**  
  - Carpeta donde se encuentran los dos pipelines de Jenkins para desplegar y detener la aplicación de Flask de la VM1.
- **`videos/`**  
  - Carpeta con vídeos demostrativos.  
  - Cada vídeo está documentado con un pequeño README.
> Esta rama sirve de punto de partida y contiene los conectores, los pipelines de Jenkins y los vídeos demostrativos.

---

## Rama `okta`
Contiene la versión de la aplicación Flask **integrada con Okta** como sistema de autenticación.
- **`APPWITHFLASK/`** – Carpeta donde se encuentra el código de la aplicación web Flask y el resto de archivos necesarios.
- **`APPWITHFLASK/app.py`** – Archivo con el código de la aplicación web Flask, haz click [aquí](https://github.com/pablofc18/myApp/blob/okta/APPWITHFLASK/app.py) para verlo.
> Haz click [aquí](https://github.com/pablofc18/myApp/tree/okta) para ir a la rama.

---

## Rama `dual_run`
Esta rama implementa la **fase de dual-run**, donde la aplicación soporta simultáneamente: **Okta** y **Microsoft Entra ID**.
- **`APPWITHFLASK/`** – Carpeta donde se encuentra el código de la aplicación web Flask y el resto de archivos necesarios.
- **`APPWITHFLASK/app.py`** – Archivo con el código de la aplicación web Flask, haz click [aquí](https://github.com/pablofc18/myApp/blob/okta/APPWITHFLASK/app.py) para verlo.
> Haz click [aquí](https://github.com/pablofc18/myApp/tree/dual_run) para ir a la rama.

---

## Rama `entraid`
Contiene la versión finalizada de la migración de la aplicación **integrada con Microsoft Entra ID**.
- **`APPWITHFLASK/`** – Carpeta donde se encuentra el código de la aplicación web Flask y el resto de archivos necesarios.
- **`APPWITHFLASK/app.py`** – Archivo con el código de la aplicación web Flask, haz click [aquí](https://github.com/pablofc18/myApp/blob/okta/APPWITHFLASK/app.py) para verlo.
> Haz click [aquí](https://github.com/pablofc18/myApp/tree/entraid) para ir a la rama.

---

> Se destaca que aparecen secretos en los archivos de logs y archivos que NO deberían estar en un proyecto estándar, en este caso todo lo que se puede observar se muestra de manera intencionada a efectos demostrativos y no tiene ninguna afectación al proyecto.
