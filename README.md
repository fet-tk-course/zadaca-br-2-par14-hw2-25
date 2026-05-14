[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/wxDq4rbD)
# Zadaća 2 - REST API aplikacija

## O projektu

[Ovdje ukratko opišite domenu vaše aplikacije i njenu svrhu]

## Tim

- **Student A**: [Ime Prezime] - resurs: `/resursi_a`
- **Student B**: [Ime Prezime] - resurs: `/resursi_b`

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

## Korištenje AI alata

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

## Napomene

[Dodatne napomene specifične za vašu implementaciju]

##  Zadaci sa provjere - Student C 

Z1:

Dodan strani ključ user_id u model Reservation, koji povezuje rezervaciju s korisnikom (User).
Implementiran POST endpoint za kreiranje korisnika i rezervacija.

Z2:

Dodana validacija u modele (UserCreate, ReservationCreate):
Ime korisnika ne smije biti prazan string.
Cijena rezervacije mora biti pozitivna.
U POST endpointima dodana provjera za jedinstvena polja (npr. email za korisnika, kombinacija seat_id i screening_id za rezervaciju) – vraća HTTP 409 ako već postoji.
Dodan custom GET endpoint za broj aktivnih korisnika.

1.POST/users/

primjer zahtjeva:

{
  "first_name": "Amina",
  "last_name": "Test",
  "email": "amina@example.com",
  "age": 22,
  "phone_number": "061123456"
}
 
 odgovor:

 {
  "id": 1,
  "first_name": "Amina",
  "last_name": "Test",
  "email": "amina@example.com",
  "age": 22,
  "phone_number": "061123456",
  "is_active": true
}

Greska, ako emai vec postoji;

{
  "detail": "Korisnik sa ovim emailom već postoji"
}

Status: 409 Conflict

2. POST /reservations/
Zahtjev:

{
  "user_id": 1,
  "screening_id": 2,
  "seat_id": 5,
  "price": 10.0
}

odgovor:

{
  "id": 1,
  "user_id": 1,
  "screening_id": 2,
  "seat_id": 5,
  "price": 10.0,
  "confirmed": false
}
greska:

{
  "detail": "Rezervacija za ovo mjesto već postoji"
}

Status:409 Conflict 

3. GET /users/active_count

Odgovor:

{
  "ukupno_aktivnih": 3
}

first_name u UserCreate ne smije biti prazan string.
Greška: "Ime ne smije biti prazan string" – HTTP 422 Unprocessable Entity
price u ReservationCreate mora biti pozitivan broj.
Greška: "Cijena mora biti pozitivna" – HTTP 422 Unprocessable Entity
Ako se pokuša kreirati korisnik s već postojećim emailom ili rezervacija za isto mjesto i projekciju, vraća se HTTP 409 Conflict.





