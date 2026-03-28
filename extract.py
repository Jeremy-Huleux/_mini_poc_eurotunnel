import requests
import psycopg2
import os
from datetime import datetime
from dotenv import load_dotenv

# On charge les variables .env
load_dotenv()

# 1. Nos clés et adresses
# On récupère la clé
API_KEY = os.getenv("OPENWEATHER_API_KEY") 

if not API_KEY:
    raise ValueError("Erreur: La clé API est introuvable. Vérifiez votre fichier .env")
CITY = "Calais,FR"
URL = f"http://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={API_KEY}&units=metric"

# 2. On va chercher la donnée (Extract)
print(f"- Interrogation de l'API pour {CITY}...")
response = requests.get(URL)
data = response.json()

# On extrait les infos qui nous intéresses (Vent et Météo)
temp = data['main']['temp']
wind_speed = data['wind']['speed']
weather_desc = data['weather'][0]['description']
timestamp = datetime.now()

print(f"- Données reçues : {temp}°C, Vent: {wind_speed} m/s, Temps: {weather_desc}")

# 3. On charge la donnée (Load)
print("- Connexion à la base de données...")
conn = psycopg2.connect(
    dbname=os.getenv("DB_NAME"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    host=os.getenv("DB_HOST"),
    port=os.getenv("DB_PORT")
)
cursor = conn.cursor()

# On crée la table si elle n'existe pas encore
cursor.execute("""
    CREATE TABLE IF NOT EXISTS raw_weather (
        id SERIAL PRIMARY KEY,
        city VARCHAR(50),
        temperature FLOAT,
        wind_speed FLOAT,
        description VARCHAR(100),
        date_extracted TIMESTAMP
    );
""")

# On insère notre relevé météo
cursor.execute("""
    INSERT INTO raw_weather (city, temperature, wind_speed, description, date_extracted)
    VALUES (%s, %s, %s, %s, %s);
""", (CITY, temp, wind_speed, weather_desc, timestamp))

# On valide la transaction et on ferme
conn.commit()
cursor.close()
conn.close()

print("- Pipeline terminé avec succès.")