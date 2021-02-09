# Sit-booking

Python-script for å booke time på Sit-treningssentre.

## Bruk

```sh
usage: book.py [-h] [--senter {gløshaugen,dragvoll,portalen,moholt}] --tid
               hhmm [--dager DAGER]
               brukernavn passord

Book treningstid hos Sit

positional arguments:
  brukernavn            Feide-brukernavn
  passord               Feide-passord

optional arguments:
  -h, --help            show this help message and exit
  --senter {gløshaugen,dragvoll,portalen,moholt}
                        treningssenter
  --tid hhmm            starttid
  --dager DAGER         antall dager frem i tid det skal bookes
```

### Eksempel

Booke time på Gløshaugen treningssenter kl. 07:30 om én dag (i morgen):
```sh
python book.py brukernavn passord --senter gløshaugen --tid 0730 --dager 1
```