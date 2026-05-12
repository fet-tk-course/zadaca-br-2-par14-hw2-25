[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/wxDq4rbD)
# Zadaća 2 - REST API aplikacija

## O projektu

[Ovdje ukratko opišite domenu vaše aplikacije i njenu svrhu]

## Tim

- **Student A**: [Ime Prezime] - resurs: `/resursi_a`
- **Student B**: [Ime Prezime] - resurs: `/resursi_b`
- **Student C**: [Amina Sarhatlic] - resurs: `/resursi_c`

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

### Resurs A: `/resursi_a`

| Metoda | Ruta | Opis |
|--------|------|------|
| GET | `/resursi_a` | Lista svih resursa (sa query filterom) |
| GET | `/resursi_a/{id}` | Dohvatanje resursa po ID-u |
| POST | `/resursi_a` | Kreiranje novog resursa |
| PUT | `/resursi_a/{id}` | Potpuna zamjena resursa |
| PATCH | `/resursi_a/{id}` | Djelimično ažuriranje resursa |
| DELETE | `/resursi_a/{id}` | Brisanje resursa |

**Primjer zahtjeva:**
```bash
# Kreiranje novog resursa
curl -X POST "http://localhost:8000/resursi_a" \
  -H "Content-Type: application/json" \
  -d '{"polje1": "vrijednost", "polje2": 123}'
```

### Resurs B: `/resursi_b`

[Analogno kao za Resurs A]

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

### Alat: [GitHub Copilot / ChatGPT / ...]
**Model:** [GPT-4, Copilot model, ...]

**Primjer 1:**
- **Prompt:** [Npr. "Kreiraj SQLModel klasu za entitet Knjiga sa poljima naslov, autor, godina, isbn"]
- **Kako je pomoglo:** [Opis]
- **Prilagodbe:** [Da li ste morali prilagoditi generisani kod]

**Primjer 2:**
- **Prompt:** [Npr. "Implementiraj PATCH endpoint sa exclude_unset=True"]
- **Kako je pomoglo:** [Opis]
- **Prilagodbe:** [Opis]

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

[Dodatne napomene specifične za vašu implementaciju]