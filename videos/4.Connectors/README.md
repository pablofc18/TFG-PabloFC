# Videos dels connectors

### [`1.0.connectors-users-groups.mp4`](https://github.com/pablofc18/myApp/blob/master/videos/4.Connectors/1.0.connectors-users-groups.mp4)

- **Explicació:**  
  En aquest vídeo es mostra el funcionament dels connectors pas a pas per extreure la info d'Okta i carregar-la a Entra ID.
  1. Primer s'observa com al portal de Microsoft Entra ID no hi ha usuaris ni grups creats.
  2. Després, s'executa la comanda `source ../APPWITHFLASK/myenv/bin/activate` que activa l'entorn virtual de Python, on s'han instal·lat les llibreries necessàries per l'app de Flask i els connectors.
  3. Seguidament, s'executen els 3 diferents scripts `extract_data.py`, `transform_data.py` i `load_data.py` que generen els diferents arxius encriptats:
    - *users.json.enc* | *groups.json.enc* 
      > Extrets del **extract_data** script, contenen la info d'Okta.
        - A les imatges [`1.3.info-groupsOkta.jpg`](https://github.com/pablofc18/myApp/blob/master/videos/4.Connectors/1.3.info-groupsOkta.jpg) i [`1.4.info-usersOkta.jpg`](https://github.com/pablofc18/myApp/blob/master/videos/4.Connectors/1.4.info-usersOkta.jpg) pots observar els usuaris i grups a Okta.
    - *users.entraid.json.enc* | *groups.entraid.json.enc*
      > Extrets del **transform_data** script, contenen la info un cop adaptada al format d'Entra ID.
    - Els següents fitxers no estan encriptats: *BATCH_RESP_U.json* i *BATCH_RESP_G.json*
      > Extrets del **load_data** script, contenen la informació retornada d'Entra ID després de la creació d'usuaris i grups.
  4. Per últim, es mostra al portal d'Entra ID els usuaris que s'han creat i els grups juntament amb els membres de cada grup.
  > Es pot observar a les imatges [`1.1.groupsjson-exampleTransformation.jpg`](https://github.com/pablofc18/myApp/blob/master/videos/4.Connectors/1.1.groupsjson-exampleTransformation.jpg) i [`1.2.usersjson-exampleTransformation.jpg`](https://github.com/pablofc18/myApp/blob/master/videos/4.Connectors/1.2.usersjson-exampleTransformation.jpg) el contingut a l'esquerra dels arxius *.json.enc (extrets de **extract_data.py**) i a la dreta un cop transformats *.entraid.json.enc (extrets de **transform_data.py**), abans d'encriptar els arxius.
