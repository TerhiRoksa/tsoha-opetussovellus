Opetussovellus/harjoitustyö

4.2.2023 Sovelluksen tilanne:

Sovellukseen voi luoda käyttäjätunnuksen ja kirjautua sisään ja ulos.
Uuden verkkokurssin voi luoda. Siihen voi lisätä materiaalia ja kysymyksiä. 
Kysymyksiin voi vastata.

Käyttäjiä ei ole vielä eriytetty opettajiin ja oppilaisiin.
Kursseja on vielä vain yksi.

Sovelluksen käynnistysohje:

Kloonaa tämä repositorio omalle koneellesi ja siirry sen juurikansioon.
Luo kansioon .env-tiedosto ja määritä sen sisältö seuraavanlaiseksi:

DATABASE_URL=<tietokannan-paikallinen-osoite>
SECRET_KEY=<salainen-avain>

Seuraavaksi aktivoi virtuaaliympäristö ja asenna sovelluksen riippuvuudet komennoilla

$ python3 -m venv venv
$ source venv/bin/activate
$ pip install -r ./requirements.txt

Määritä vielä tietokannan skeema komennolla

$ psql < schema.sql

Nyt voit käynnistää sovelluksen komennolla

$ flask run


Tavoite/Lähtötilanne:

Sovellus toteutetaan Pythonilla Flask-kirjastolla käyttäen 
PostgreSQL-tietokantaa,sekä GitHub- ja 
Fly.io-palveluja.

Sovelluksessa voidaan luoda verkkokursseja ja osallistua verkkokursseille. 
Verkkokurssilla on opetusmateriaalia ja automaattisesti tarkastettavia tehtäviä. 
Sovelluksen käyttäjä on joko opettaja tai opiskelija.

Sovelluksen ominaisuuksia:

Käyttäjä voi luoda uuden tunnuksen, kirjautua sisään ja ulos.

Opiskelija näkee listan kursseista ja voi liittyä kurssille.
Opiskelija voi lukea kurssin materiaalia ja tehdä kurssin tehtäviä.
Opiskelija näkee tilaston suorittamistaan tehtävistä.

Opettaja voi luoda uuden kurssin, muuttaa olemassa olevaa kurssia ja poistaa kurssin.
Opettaja pystyy lisäämään kurssille materiaalia ja tehtäviä.
Opettaja näkee kurssinsa opiskelijat ja heidän tekemät tehtävät.

