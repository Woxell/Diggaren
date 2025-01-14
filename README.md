# SRotify API (Diggaren, grupp 17)

Detta projekt tillhandahåller funktionalitet för att lyssna på radiostationer från Sveriges Radio samt söka efter låtar på Spotify baserat på vad som spelas just nu i en radiostation.

Följ stegen nedan för att ställa in din utvecklingsmiljö.

## Python

Se till att du har Python 3.x installerat på din dator. Du kommer även att behöva pip för att hantera beroenden.

## Klona repot från Github

Klona detta repo till valfri mapp på din dator: https://github.com/Woxell/Diggaren/

## Requirements.txt
I terminalen navigera till projektets src-mapp där requirements.txt-filen är. Skriv följande kommando för att installera nödvändiga beroenden.

##### Alternativ 1
pip install -r requirements.txt

##### Alternativ 2
pip3 install -r requirements.txt

## Spotify API-nycklar
I src-mappen ska där finnas en textfil 'spotify-api-key.txt' innehållande en API- och Secret-nyckel. Saknas detta, kontakta någon i Grupp 17 för att få rätt nycklar.

#### Spotify-användare
Till API:t måste man whitelistas. Om du inte är det, be André göra det genom att du skickar han din e-post som du använder för inloggning till Spotify. 
## Starta API:t
Starta API:t genom att köra main.py

## Webbgränssnitt
I valfri webbläsare, gå till [localhost:5000]() eller http://127.0.0.1:5000

### Funktioner

#### Välja radiostation
Välj en radiostation att lyssna på genom att klicka på en av radiostationernas länkar i listan till vänster.

#### Informationsavsnitt
I avsnittet uppe till höger syns information om radiokanalen som spelas just nu samt spelkontroller för ljudströmmen.

#### Sök-knappar
För nuvarande eller föregående låt kan man välja att göra en sökning på Spotify. En länk genereras som tar en till Spotify för just den låten som spelats (med hög sannolikhet).

#### Sökresultat
I avsnittet nere till höger syns de senaste fem sökningarna.

## API-dokumentation
För att se API-dokumentation, gå till [localhost:5000/api]() eller öppna api.html-filen i valfri webbläsare.