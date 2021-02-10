# Sit-booking

Python-script for å booke egentrening på Sit-treningssentre.

## Krav

- Python 3
- Selenium
- Google Chrome
- Chrome-driver for Selenium

## Bruk

```
usage: book.py [-h] --tid hhmm [--dager DAGER] [--max-forsøk MAX_FORSØK]
               [--senter {gløshaugen,dragvoll,portalen,moholt}]
               brukernavn passord

Book egentreningstid hos Sit.

positional arguments:
  brukernavn            Feide-brukernavn
  passord               Feide-passord

optional arguments:
  -h, --help            show this help message and exit
  --tid hhmm            starttid (eksempel: 0730)
  --dager DAGER         antall dager frem i tid det skal bookes (default: 2)
  --max-forsøk MAX_FORSØK
                        Maks. antall forsøk på å booke (default: 2)
  --senter {gløshaugen,dragvoll,portalen,moholt}
                        treningssenter (default: gløshaugen)
```

### Eksempel

Booke time på Gløshaugen treningssenter kl. 07:30 om én dag (i morgen):
```sh
python book.py brukernavn passord --tid 0730 --dager 1 --senter gløshaugen
```

## Lisens

[MIT](LICENSE).