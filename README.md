# Porównywarka cen kart graficznych między wybranymi sklepami

Aplikacja napisana w celu nauki pythona oraz dockera, a także jako temat do pracy inżynierskiej.

## Uruchomienie aplikacji w środowisku lokalnym

Aby uruchomić aplikację lokalnie należy:\
-`git pull` - ściągnąć kod\
-`docker-compose up` - uruchomić kontenery\
-`docker-compose run db mysql -u username -p djangoapp-db < djangoapp-db.sql` LUB za pomocą panelu dostępnego pod adresem localhost:80 - importować bazę danych\
\- otworzyć stronę  localhost:8000 w przeglądarce

## Uruchomienie web scraperów

-`python3 -m venv .` - stworzenie virtual environment\
-`python3 -m pip install selenium` - instalacja biblioteki selenium\
-`python3 ./scrapers/morele/main.py`\
-`python3 ./scrapers/komputronik/main.py`\

## implementacja + opis użytkowy z pracy inżynierskiej

![strona 1](./readme-files/page-0001.png)
![strona 2](./readme-files/page-0002.png)
![strona 3](./readme-files/page-0003.png)
![strona 4](./readme-files/page-0004.png)
![strona 5](./readme-files/page-0005.png)
![strona 6](./readme-files/page-0006.png)
![strona 7](./readme-files/page-0007.png)
![strona 8](./readme-files/page-0008.png)
![strona 9](./readme-files/page-0009.png)
![strona 10](./readme-files/page-0010.png)
![strona 11](./readme-files/page-0011.png)
![strona 12](./readme-files/page-0012.png)
![strona 13](./readme-files/page-0013.png)
![strona 14](./readme-files/page-0014.png)
![strona 15](./readme-files/page-0015.png)
![strona 16](./readme-files/page-0016.png)
![strona 17](./readme-files/page-0017.png)
![strona 18](./readme-files/page-0018.png)
![strona 19](./readme-files/page-0019.png)
![strona 20](./readme-files/page-0020.png)
![strona 21](./readme-files/page-0021.png)
![strona 22](./readme-files/page-0022.png)
![strona 23](./readme-files/page-0023.png)
![strona 24](./readme-files/page-0024.png)
![strona 25](./readme-files/page-0025.png)
![strona 26](./readme-files/page-0026.png)
