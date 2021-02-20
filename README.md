# Sit-booking

Python-script for å booke egentrening på Sit-treningssentre.

## Krav

- Python 3
- Se [`requirements.txt`](requirements.txt)

## Bruk

```
usage: book.py [-h] --time hhmm [--days DAYS]
               [--studio {gløshaugen,dragvoll,portalen,dmmh,moholt}]
               username password

Book training slots (egentrening) at Sit.

positional arguments:
  username              Sit username (email)
  password              Sit password

optional arguments:
  -h, --help            show this help message and exit
  --time hhmm           start time (example: 0730) (default: None)
  --days DAYS           number of days until training slot (0 is today)
                        (default: 2)
  --studio {gløshaugen,dragvoll,portalen,dmmh,moholt}
                        studio (default: gløshaugen)
```

### Eksempel

Booke time på Gløshaugen treningssenter kl. 15:30 om to dager:
```
$ python book.py per@example.com passord123 --time 1530 --days 2 --studio gløshaugen
```

## Lisens

[MIT](LICENSE).