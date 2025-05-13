# Repositori TFG PabloFC 

Aquest repositori conté el codi de la app Flask en les diferents fases de la migració i el material suplementari (videos, connectors)

---

## Estructura de la branca `master`

En la branca `master` trobaràs:

- **`connectors/`**  
  Carpeta amb scripts i mòduls de connexió als diferents serveis d’autenticació.  
  - Clica sobre cada fitxer per veure’n el codi i la documentació integrada.  
- **`videos/`**  
  Carpeta amb vídeos demostratius.  
  - Cada vídeo està documentat amb un petit README.

> Aquesta branca serveix de punt de partida i conté només els connectors i els vídeos.

---

## Branca `okta`

Conté la versió de l’aplicació Flask **integrada amb Okta** com a sistema d’autenticació.

- **`APPWITHFLASK/`** – Codi de l'aplicació web Flask integrat amb Okta.

> Per veure aquest codi, canvia de branca amb:
> ```bash
> git switch okta
> ```

---

## Branca `dual_run`

Aquesta branca implementa la **fase de dual-run**, on l’aplicació suporta simultàniament:

1. **Okta**  
2. **Microsoft Entra ID**

- **`APPWITHFLASK/`** – Codi de l'aplicació web Flask integrat amb Okta i Entra ID.

> Canvia a aquesta branca amb:
> ```bash
> git switch dual_run
> ```

---

## Branca `entraid`

Conté la versió finalitzada la migració de l’aplicació **integrada amb Microsoft Entra ID**.

- **`app/`** – Codi de l'aplicació Flask integrat amb Microsoft Entra ID.

> Per accedir-hi:
> ```bash
> git switch entraid
> ```

---
