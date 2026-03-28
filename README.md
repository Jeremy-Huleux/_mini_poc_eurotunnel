# 🚄 Eurotunnel Weather & Traffic Pipeline (Mini-POC)

## 🎯 Objectif Métier
Ce projet est un Proof of Concept (POC) de Data Engineering visant à croiser les conditions météorologiques du détroit du Pas-de-Calais avec les enjeux de trafic d'Eurotunnel (Getlink). 

**Le contexte :** Une tempête ou des vents violents empêchent les ferries (DFDS, P&O) de sortir du port, ce qui reporte massivement et en urgence le trafic fret et passagers sur le tunnel sous la Manche, créant des congestions majeures. Ce pipeline ingère, stocke et transforme la donnée météorologique brute pour créer des statuts d'alerte automatisés, première étape pour anticiper ces pics d'affluence.

## 🛠️ Stack Technique
* **Extraction (Extract) :** Python (`requests`) via l'API OpenWeatherMap.
* **Base de données (Load) :** PostgreSQL.
* **Infrastructure :** Docker & Docker Compose.
* **Transformation (Transform) :** dbt (Data Build Tool).
* **Sécurité :** Gestion des secrets via variables d'environnement (`.env`).

## 📋 Prérequis
Avant de lancer ce projet, assurez-vous d'avoir installé sur votre machine :
- [Docker](https://www.docker.com/) et Docker Compose.
- [Python 3.8+](https://www.python.org/).
- Un compte gratuit sur [OpenWeatherMap](https://openweathermap.org/) pour obtenir une clé API.

## 🚀 Guide d'installation et d'exécution

### 1. Cloner le projet
```bash
git clone [https://github.com/VOTRE_NOM_UTILISATEUR/poc-eurotunnel-data.git](https://github.com/VOTRE_NOM_UTILISATEUR/poc-eurotunnel-data.git)
cd poc-eurotunnel-data
```

### 2. Configuration et Sécurité (Le fichier .env)
Ce projet utilise des variables d'environnement pour sécuriser les mots de passe et les clés API.
1. Allez sur [OpenWeatherMap](https://openweathermap.org/), créez un compte gratuit et récupérez votre clé API dans la section "My API keys".
2. À la racine du projet, copiez le fichier d'exemple pour créer votre propre fichier de configuration :
   * Sous Linux/Mac : `cp .env.example .env`
   * Sous Windows : `copy .env.example .env`
3. Ouvrez le fichier `.env` nouvellement créé et insérez votre clé API à la ligne `OPENWEATHER_API_KEY=...`. Vous pouvez laisser les autres paramètres de base de données par défaut pour un test local.

### 3. Lancer l'infrastructure (Base de données)
Démarrez le conteneur PostgreSQL en arrière-plan :
```bash
docker compose up -d
```
*(La base de données sera accessible sur le port défini dans votre fichier `.env`, par exemple 5433).*

### 4. Préparer l'environnement Python
Créez un environnement virtuel isolé et installez les dépendances :
```bash
python -m venv venv
# Activation sous Windows : venv\Scripts\activate
# Activation sous Mac/Linux : source venv/bin/activate

pip install -r requirements.txt
```
*(Note : Si vous n'avez pas de fichier requirements.txt, lancez simplement : `pip install requests psycopg2-binary python-dotenv dbt-postgres`)*

### 5. Lancer l'ingestion de données (Extract & Load)
Exécutez le script Python pour interroger l'API Météo et charger la donnée brute dans PostgreSQL :
```bash
python extract.py
```

### 6. Lancer la transformation métier (Transform avec dbt)
Naviguez dans le dossier dbt et lancez la compilation des modèles pour créer les tables d'alertes finalisées :
```bash
cd transform_eurotunnel
dbt run
```

🎉 **C'est terminé !** Les données nettoyées, converties (km/h) et enrichies (statuts d'alerte) sont maintenant disponibles dans le schéma `analytics` de la base de données, prêtes à être connectées à un outil de BI.