# D&D Muistikirja - Tietokantasovellus

Sovelluksen tämänhetkisiä ominaisuuksia:
- Käyttäjä voi luoda itselleen tunnukset. Jos tunnukset ovat ensimmäiset luodut tunnukset, on käyttäjä admin, muuten user.
- Käyttäjä voi kirjautua sisään ja ulos.
- Käyttäjä näkee etusivulla listan pelissä käytetyistä alueista.
- Käyttäjä voi avata alueen tiedot klikkaamalla aluetta etusivulta.
- Käyttäjä voi luoda itselleen henkilökohtaisia muistiinpanoja, jotka eivät näy muille käyttäjille. Muistiinpanoja voi muokata ja jos sen tallettaa tyhjänä, se poistuu.
- Admin voi luoda uuden alueen ja muokata alueiden tietoja, niin että ne näkyvä kaikille.
- Käyttäjä näkee etusivulla listan pelin kaikista npc hahmoista ja voi klikata sen auki, missä näkyy npc:n tiedot.
- Käyttäjä näkee jokaisella alueella sen alueen npc:t ja voi klikata ne auki ja katsoa niiden tietoja.
- Admin voi luoda uuden npc:n ja muokata vanhojen tietoja, sekä asettaa ne tietylle alueelle.

## Kuinka käyttää ja testata sovellusta komentoriviltä
**1)** Aluksi kopioi projekti koneellesi GitHubista


**2)** Luo Pythonin virtuaaliympäristö projektikansioon:

```bash
python3 -m venv venv
```

**3)** Ja käynnistä virtuaaliympäristö:

```bash
source venv/bin/activate
```

**4)** Ympäristön riippuvuudet löytyvät tiedostosta [requirements.txt](./requirements.txt). 
Nämä voit asentaa kerralla:

```bash
pip install -r requirements.txt
```


**5)** Käytössä on Postgres-tietokanta. Skeema löytyy tiedostosta [schema.sql](./schema.sql). Pääset luomaan taulut tietokantaan:

```bash
psql < schema.sql
```

**6)** Tämän jälkeen pääset käynnistämään ohjelman virtuaaliympäristöstä:

```bash
flask run
```
