# Tracke medisiner

Applikasjonen har som formål å holde styr på at melk og medisin jeg tar ikke kombineres. Medisinen krever at man ikke tar melkeprodukter 1time før og etter medisininntak.
Under følger en lett dokumentasjonen av webapplikasjonen som er bygget med Flask og Vue.js
## Arkitektur

### Backend

- **`models.py`**: Inneholder definisjoner av databasemodellene for `User`, `MilkLog`, og `PillLog`.
- **`routes.py`**: Ansvarlig for håndtering av ruter/endepunkter for funksjonaliteter som registrering, innlogging, logging av melk og medisin, samt henting av logger.

### Frontend

#### Komponenter

Appen består av flere Vue-komponenter for ulike deler av brukergrensesnittet (UI), inkludert:

- **`Home.vue`**: Hovedsiden som viser brukerstatus og tilbyr funksjonalitet for å logge melk- og medisininntak.
- **`SignUp.vue`** og **`LogIn.vue`**: Skjemaer for brukerregistrering og innlogging.
- **`ProfileDash.vue`**: En brukerprofilside som viser detaljert logginformasjon og tilbyr redigeringsmuligheter.

#### Routing

- Bruker Vue Router for å håndtere navigasjon mellom de forskjellige sidene/komponentene.

## API Dokumentasjon

### Endepunkter

- **POST `/register`**: Registrer en ny bruker.
- **POST `/login`**: Logg inn en eksisterende bruker.
- **POST `/logout`**: Logg ut den nåværende brukeren.
- **POST `/drink_milk`**: Legg til en melkelogg for den innloggede brukeren.
- **POST `/take_pill`**: Legg til en pillelogg for den innloggede brukeren.
- **GET `/can_i`**: Hent status for om brukeren kan ta melk eller medisin.

## Sikkerhet og autentisering

- Autentisering håndteres ved hjelp av Flask-Login for å støtte innloggingssesjoner.
- Passord hashes før de lagres i databasen ved hjelp av `werkzeug.security`.
