# Porównywarka cen kart graficznych między wybranymi sklepami

Aplikacja porównująca ceny między obecnie dwoma sklepami internetowymi.

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

## Rzeczy do zrobienia
- obserwowanie produktów przez użytkowników - panel dla użytkownika + wiadomość zaobserwowano/odobserwowano;
- średnia cen czy rynek rośnie czy maleje;
- podział na produkty dostępne w obu / w jednym sklepie;
- wygląd kafelków produktów na liście wszystkich prod.;

