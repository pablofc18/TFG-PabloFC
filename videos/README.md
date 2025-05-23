# Carpeta `videos`

Aquest directori conté diversos vídeos demostratius i les seves captures associades. Els videos i captures es separen en 3 diferents fases, amb la integració d'Okta, amb la integració d'ambdós (fase dual-run) i amb la integració de Microsoft Entra ID. Més informació de cadascun es pot trobar dins de la seva respectiva carpeta.

---

## Integrats amb `Okta`

- Es troben a la carpeta [**Okta**](https://github.com/pablofc18/myApp/blob/master/videos/Okta)

## Integrats amb `Okta i EntraID` (**dual-run**)

- Es troben a la carpeta  [**Dual_run**](https://github.com/pablofc18/myApp/blob/master/videos/Dual_run)

## Integrats amb `Microsoft Entra ID`

- Es troben a la carpeta  [**EntraID**](https://github.com/pablofc18/myApp/blob/master/videos/EntraID)

---
---

- El següent video no correspon a cap integració com a tal.   

### [`connectors-EntraID-u-g.mp4`](https://github.com/pablofc18/myApp/blob/master/videos/connectors-EntraID-u-g.mp4)

- **Explicació:**  
  En aquest vídeo es mostra el funcionament dels connectors pas a pas per extreure la info d'Okta i carregar-la a Entra ID.
  1. Primer s'observa com al portal de Microsoft Entra ID no hi ha usuaris ni grups creats.
  2. Després, s'executa la comanda `source ../APPWITHFLASK/myenv/bin/activate` que activa l'entorn virtual de Python, on s'han instal·lat les llibreries necessàries per l'app de Flask i els connectors.
  3. Seguidament, s'executen els 3 diferents scripts `extract_data.py`, `transform_data.py` i `load_data.py` que generen els diferents arxius encriptats:
    - *users.json.enc* | *groups.json.enc* 
      > Extrets del **extract_data** script, contenen la info d'Okta.
        - A les imatges [`info-usersOkta.jpg`](https://github.com/pablofc18/myApp/blob/master/videos/info-usersOkta.jpg) i [`info-groupsOkta.jpg`](https://github.com/pablofc18/myApp/blob/master/videos/info-groupsOkta.jpg) pots observar els usuaris i grups a Okta.
    - *users.entraid.json.enc* | *groups.entraid.json.enc*
      > Extrets del **transform_data** script, contenen la info un cop adaptada al format d'Entra ID.
    - Els següents fitxers no estan encriptats: *BATCH_RESP_U.json* i *BATCH_RESP_G.json*
      > Extrets del **load_data** script, contenen la informació retornada d'Entra ID després de la creació d'usuaris i grups.
  4. Per últim, es mostra al portal d'Entra ID els usuaris que s'han creat i els grups juntament amb els membres de cada grup.
  > Es pot observar a les imatges [`usersjson-example.jpg`](https://github.com/pablofc18/myApp/blob/master/videos/usersjson-example.jpg) i [`groupsjson-example.jpg`](https://github.com/pablofc18/myApp/blob/master/videos/groupsjson-example.jpg) el contingut a l'esquerra dels arxius *.json.enc (extrets de **extract_data.py**) i a la dreta un cop transformats *.entraid.json.enc (extrets de **transform_data.py**), abans d'encriptar els arxius.

