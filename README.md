# Pràctica 1: Quin és el pronòstic del futur guanyador d’Eurovisió 2023 segons les seves aliances geopolítiques?
***Scrapping Eurovision 2023***

## Descripció

Aquesta projecte s'ha realitzat sota el context de l'assignatura Tipologia i cicle de vida de les dades, del Màster en Ciència de Dades de la Universitat Oberta de Catalunya. S'hi apliquen tècniques de web scraping mitjançant el llenguatge de programació Python per extreur dades de la web [EurovisionWorld](https://eurovisionworld.com/odds/eurovision) i generar cinc dataset.

**Atenció: es fa ús de WebDriver amb l'eina de Google Chrome com navegador. Tingeu present d'actualitzar aquest a la versió més recent.**

## Fitxers del codi font

* **dataset/20221114**: magatzem dels CSV on la subcarpeta 20221114 correspon a any-mes-dia de l'extracció dels CSV via scraping.
* **requirements.txt**: llibreries i versions utilitzades
* **source/**: carpeta modular on es localitza tot el codi font en llenguatge Python.
  * **source/main.py**: punt de partida. S'inicia el procés de scraping.
  * **source/module**: subcarpeta on es localitza codi python dividits per moduls.
    * **source/module/api_twitter.py**: extracció en CSV de tweets sota l'API Twitter
    * **source/module/bet_house_2023.py**: extracció en CSV de les quotes de mercat del país guanyador Eurovisió 2023
    * **source/module/commons.py**: scrapping de totes les nacions per a Eurovisió amb els anys respectius i generador csv
    * **source/module/countries.py**: extracció del nom de tots els pïsos
    * **source/module/historic_country.py**: extracció en CSV de la performance del festival de cada any.
    * **source/module/poll_2022.py**: extracció en CSV de l'enquesta 'Qui guanyarà Eurovisió al 2022?'
    * **source/module/scoreboard.py**: extraccció de cross-table de vots entre tots el països.
    * **source/module/chromedriver**: subcarpeta on es configura ChromeDriver
      * **source/module/chromedriver/chrome_driver.py**: configuració del User-Agent i entre d'altres opcions del WebDriver Chrome.
      * **source/module/chromedriver/chrome_driver.exe**: l'interfície WebDriver per iniciar el navegador Google Chrome via Selenium.

## Dataset
EL DOI del data set en format CSV:  https://doi.org/10.5281/zenodo.7323675

## Autors
* Jordi Samaniego Vidal et Antoni Espadas Navarro
