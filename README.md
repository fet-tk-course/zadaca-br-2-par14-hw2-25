[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/wxDq4rbD)
# Zadaća 2 - REST API aplikacija

## O projektu

Aplikacija predstavlja backend sistem za upravljanje kino repertoarom.
Omogućava evidenciju filmova i žanrova, a planirana je evidencija sala, 
projekcija, korisnika i rezervacija.

## Tim

- **Student A**: Nejla Kavazović - resurs: `/genres`, `/movies`
- **Student B**: Elnur Bjelić - resurs: `/seat-types`, `/hall-types`, `/halls`, `/seats`, `/screenings`
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
| Metoda | Ruta | Opis |
| --- | --- | --- |
| GET | /genres | Lista svih žanrova (filter: ?is_active=true/false) |
| GET | /genres/{id} | Dohvatanje žanra po ID-u |
| POST | /genres | Kreiranje novog žanra (status 201) |
| PUT | /genres/{id} | Potpuna zamjena žanra |
| PATCH | /genres/{id} | Djelimično ažuriranje žanra |
| DELETE | /genres/{id} | Brisanje žanra (status 204) |

### Filmovi `/movies`
| Metoda | Ruta | Opis |
| --- | --- | --- |
| GET | /movies | Lista svih filmova (filter: ?is_currently_showing=true/false) |
| GET | /movies/{id} | Dohvatanje filma po ID-u |
| POST | /movies | Kreiranje novog filma (status 201) |
| PUT | /movies/{id} | Potpuna zamjena filma |
| PATCH | /movies/{id} | Djelimično ažuriranje filma |
| DELETE | /movies/{id} | Brisanje filma (status 204) |

**Primjer zahtjeva:**

#### Kreiranje novog žanra
```bash
curl -X POST "http://localhost:8000/genres" \
  -H "Content-Type: application/json" \
  -d '{"name": "Action", "description": "Akcioni filmovi", "popularity_score": 8.5, "is_active": true}'
```

### Resurs B:

### Tipovi sjedala `/seat-types`
Metoda | Ruta | Opis
| --- | --- | --- |
GET | /seat-types | Lista svih tipova sjedala (filter: ?name=seat_type_name)
GET | /seat-types/{id} | Dohvatanje tipa sjedala po ID-u
POST | /seat-types | Kreiranje novog tipa sjedala (status 201)
PUT | /seat-types/{id} | Potpuna zamjena tipa sjedala
DELETE | /seat-types/{id} | Brisanje tipa sjedala (status 204)

### Tipovi dvorana `/hall-types`
Metoda | Ruta | Opis
| --- | --- | --- |
GET | /hall-types | Lista svih tipova dvorana (filter: ?name=hall_type_name)
GET | /hall-types/{id} | Dohvatanje tipa dvorana po ID-u
POST | /hall-types | Kreiranje novog tipa dvorana (status 201)
PUT | /hall-types/{id} | Potpuna zamjena tipa dvorana
DELETE | /hall-types/{id} | Brisanje tipa dvorana (status 204)

### Sjedala `/seats`
Metoda | Ruta | Opis
| --- | --- | --- |
GET | /seats | Lista svih sjedala (filteri: `?hall_id=broj`, `?type_id=broj`, `?type_name=string`)
GET | /seats/{id} | Dohvatanje sjedala po ID-u
POST | /seats | Kreiranje novog sjedala (status 201)
PUT | /seats/{id} | Potpuna zamjena sjedala
PATCH | /seats/{id} | Djelimično ažuriranje sjedala
DELETE | /seats/{id} | Brisanje sjedala (status 204)

### Sale `/halls`
Metoda | Ruta | Opis
| --- | --- | --- |
GET | /halls | Lista svih sala (opcionalni filter: `?type_name=string`)
GET | /halls/with-type-name | Lista svih sala sa nazivom tipa
GET | /halls/{id} | Dohvatanje sale po ID-u
GET | /halls/{id}/with-type-name | Dohvatanje sale po ID-u sa nazivom tipa
POST | /halls | Kreiranje nove sale (status 201)
PUT | /halls/{id} | Izmjena postojeće sale po ID-u
DELETE | /halls/{id} | Brisanje sale (status 204)

**Napomena:** U GET ruti za sjedala nije dozvoljeno istovremeno slati `type_id` i `type_name`.

### Projekcije `/screenings`
Metoda | Ruta | Opis
| --- | --- | --- |
GET | /screenings | Lista svih projekcija (filteri: `?hall_id=broj`, `?movie_id=broj`)
GET | /screenings/{id} | Dohvatanje projekcije po ID-u
GET | /screenings/{id}/with-details | Dohvatanje projekcije po ID-u sa podacima o sali i filmu
POST | /screenings | Kreiranje nove projekcije (status 201, provjera konflikta termina u istoj sali)
PUT | /screenings/{id} | Potpuna zamjena projekcije (provjera konflikta termina u istoj sali)
PATCH | /screenings/{id} | Djelimično ažuriranje projekcije (provjera konflikta termina u istoj sali)
DELETE | /screenings/{id} | Brisanje projekcije (status 204)

**Primjer zahtjeva:**

#### Dohvatanje detaljnih informacija o projekciji

```bash
curl -X 'GET' \
  'http://localhost:8000/screenings/1/with-details' \
  -H 'accept: application/json'
```

### Resurs C: `/resursi_c`
### Student C: Modul za upravljanje korisnicima i rezervacijama

#### Resursi i endpointi: `/student_c/users` i `/student_c/reservations`

| Metoda | Ruta | Opis |
|--------|------|-------|
| POST | `/student_c/users` | Registracija novog korisnika u sistem |
| GET | `/student_c/users` | Pregled svih korisnika (moguć filter po godinama) |
| GET | `/student_c/users/{id}` | Detaljan prikaz jednog korisnika preko ID-a |
| PATCH | `/student_c/users/{id}` | Djelimična izmjena podataka korisnika |
| DELETE | `/student_c/users/{id}` | Uklanjanje korisnika iz baze |
| GET | `/student_c/reservations` | Lista svih rezervacija u sistemu |
| POST | `/student_c/reservations` | Kreiranje nove rezervacije za sjedište |
| GET | `/student_c/reservations/{id}` | Dohvatanje detalja specifične rezervacije |
| DELETE | `/student_c/reservations/{id}` | Otkazivanje rezervacije |

**Primjer zahtjeva:**
```bash
# Kreiranje korisnika
curl -X POST "http://localhost:8000/student_c/users" \
     -H "Content-Type: application/json" \
     -d '{"first_name": "Amina", "last_name": "Test", "email": "amina@example.com", "age": 22, "phone_number": "061123456"}'
## Korištenje AI alat

Alat: Claude (Anthropic), GitHub Copilot
Model: Claude Sonnet 4.6, Copilot Model 

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

## STUDENT C:

## Korištenje AI alata

### Alat: Gemini / ChatGPT
**Model:** Gemini 1.5 Flash/GPT-4o

**Primjer 1: Validacija opcionalnih polja u PATCH metodi**
- **Prompt:** "Kako u FastAPI ruti za ažuriranje (PATCH) osigurati da se u bazu spase samo ona polja koja je korisnik poslao, bez prepisivanja ostalih polja null vrijednostima?"
- **Kako je pomoglo:** Razjašnjena je upotreba parametra `exclude_unset=True` unutar `model_dump` metode. Ovo mi je omogućilo da implementiram logiku koja čuva integritet postojećih podataka u bazi.
- **Prilagodbe:** Dobijenu logiku sam ugradila u funkciju `update_user` unutar `routes_c.py`, prilagodivši je svom modelu `UserUpdate`.

**Primjer 2: Filtriranje podataka kroz Query parametre**
- **Prompt:** "Na koji način unutar SQLModel select izraza dodati uslovno filtriranje samo ako je određena varijabla proslijeđena kao Query parametar?"
- **Kako je pomoglo:** Dobila sam uvid u to kako se `statement` objekt može postepeno nadograđivati prije izvršavanja. Ovo je bilo korisno za izradu moje GET rute za korisnike.
- **Prilagodbe:** Implementirala sam ovo u ruti `get_users`, gdje se filter po godinama (`age`) primjenjuje samo ako ga korisnik unese u Swaggeru.

**Primjer 3: Mapiranje podataka između modela**
- **Prompt:** "Kako najbrže mapirati podatke iz Pydantic 'Create' modela u SQLModel 'Table' model bez ručnog dodjeljivanja svakog polja?"
- **Kako je pomoglo:** Predložena je metoda `model_validate()`, koja automatski prebacuje podatke u bazu uz poštovanje validacije.
- **Prilagodbe:** Iskoristila sam ovaj pristup u rutama za kreiranje korisnika i rezervacija, čime je kod postao kraći i pregledniji.

## Napomene

Aplikacija je testirana na Python 3.12.10 bez virtualnog okruženja.
Za pokretanje koristiti: py -3.12 -m uvicorn main:app --reload
