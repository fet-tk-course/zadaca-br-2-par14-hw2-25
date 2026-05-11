[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/wxDq4rbD)
# Zadaća 2 - REST API aplikacija

## O projektu

Aplikacija predstavlja backend sistem za upravljanje kino repertoarom.
Omogućava evidenciju filmova i žanrova, a planirana je evidencija sala, 
projekcija, korisnika i rezervacija.

## Tim

- **Student A**: Nejla Kavazović - resurs: `/genres`, `/movies`
- **Student B**: Elnur Bjelić - resurs: `/seat-types`
- **Student C**: Ime Prezime - resurs: `/resursi-c`

## Instalacija i pokretanje

### Preduvjeti

- Python 3.10 ili noviji
- pip

### Koraci

1. Klonirajte repozitorij:
```bash
git clone <url-repozitorija>
cd <naziv-repozitorija>
```

2. Kreirajte virtuelno okruženje:
```bash
python -m venv venv
```

3. Aktivirajte virtuelno okruženje:
   - Windows: `venv\Scripts\activate`
   - Linux/Mac: `source venv/bin/activate`

4. Instalirajte zavisnosti:
```bash
pip install -r requirements.txt
```

5. Pokrenite aplikaciju:
```bash
uvicorn main:app --reload
```

6. Otvorite browser na adresi: `http://localhost:8000/docs`

## API Endpointi

### Resurs A:

### Žanrovi `/genres`
Metoda | Ruta | Opis
GET | /genres | Lista svih žanrova (filter: ?is_active=true/false)
GET | /genres/{id} | Dohvatanje žanra po ID-u
POST | /genres | Kreiranje novog žanra (status 201)
PUT | /genres/{id} | Potpuna zamjena žanra
PATCH | /genres/{id} | Djelimično ažuriranje žanra
DELETE | /genres/{id} | Brisanje žanra (status 204)

### Filmovi `/movies`
Metoda | Ruta | Opis
GET | /movies | Lista svih filmova (filter: ?is_currently_showing=true/false)
GET | /movies/{id} | Dohvatanje filma po ID-u
POST | /movies | Kreiranje novog filma (status 201)
PUT | /movies/{id} | Potpuna zamjena filma
PATCH | /movies/{id} | Djelimično ažuriranje filma
DELETE | /movies/{id} | Brisanje filma (status 204)

**Primjer zahtjeva:**

# Kreiranje novog žanra
curl -X POST "http://localhost:8000/genres" \
  -H "Content-Type: application/json" \
  -d '{"name": "Action", "description": "Akcioni filmovi", "popularity_score": 8.5, "movie_count": 0, "is_active": true}'

### Resurs B:

### Tipovi sjedala `/seat-types`
Metoda | Ruta | Opis
GET | /seat-types | Lista svih tipova sjedala (filter: ?name=seat_type_name)
GET | /seat-types/{id} | Dohvatanje tipa sjedala po ID-u
POST | /seat-types | Kreiranje novog tipa sjedala (status 201)
PUT | /seat-types/{id} | Potpuna zamjena tipa sjedala
DELETE | /seat-types/{id} | Brisanje tipa sjedala (status 204)

### Tipovi dvorana `/hall-types`
Metoda | Ruta | Opis
GET | /hall-types | Lista svih tipova dvorana (filter: ?name=hall_type_name)
GET | /hall-types/{id} | Dohvatanje tipa dvorana po ID-u
POST | /hall-types | Kreiranje novog tipa dvorana (status 201)
PUT | /hall-types/{id} | Potpuna zamjena tipa dvorana
DELETE | /hall-types/{id} | Brisanje tipa dvorana (status 204)

### Sjedala `/seats`
Metoda | Ruta | Opis
GET | /seats | Lista svih sjedala (filteri: `?hall_id=broj`, `?type_id=broj`, `?type_name=string`)
GET | /seats/{id} | Dohvatanje sjedala po ID-u
POST | /seats | Kreiranje novog sjedala (status 201)
PUT | /seats/{id} | Potpuna zamjena sjedala
DELETE | /seats/{id} | Brisanje sjedala (status 204)

**Napomena:** U GET ruti za sjedala nije dozvoljeno istovremeno slati `type_id` i `type_name`.

**Primjer zahtjeva:**

# Kreiranje nove projekcije
//To be added
## Korištenje AI alata

Alat: Claude (Anthropic)
Model: Claude Sonnet 4.6

Primjer 1:
Prompt: "Napravi SQLModel entitet za Film sa najmanje 5 polja različitih tipova, 
uključujući string, int, float, bool i Optional polja"
Kako je pomoglo: Generisana je kompletna struktura klase sa svim potrebnim poljima
Prilagodbe: Uklonjen tmdb_id, dodan director i trailer_url, ispravljeni encoding problemi

Primjer 2:
Prompt: "Implementiraj kompletne FastAPI CRUD rute za Genre i Movie entitet 
koristeći dependency injection sa Depends i SQLModel Session"
Kako je pomoglo: Generisane su sve rute uključujući exclude_unset=True za PATCH
Prilagodbe: Prilagođene poruke grešaka, usklađeni nazivi funkcija

## Napomene

Aplikacija je testirana na Python 3.12.10 bez virtualnog okruženja.
Za pokretanje koristiti: py -3.12 -m uvicorn main:app --reload
