# API EDT EPSI

### Projet déprécié : Un portail d'authentification a été ajouté sur l'EDT wigor.

Ce projet permet d'intégrer l'emploi du temps de l'EPSI à votre calendrier Google.

## Fonctionnement

Le service récupère l'emploi du temps via une requête et génère un fichier `.ics` pour intégration avec Google Calendar.

## Utilisation

### Intégration avec Google Calendar

Pour ajouter l'emploi du temps à votre Google Calendar :

1. Rendez-vous sur [Google Calendar](https://calendar.google.com/calendar/u/0/r?pli=1).
2. Allez dans les paramètres.
3. Sélectionnez "Ajouter un agenda", puis "À partir d'une URL".
4. Entrez l'URL suivante en ajustant avec vos informations personnelles :

    ```
    https://calendar.lightin.io/v1/month?firstname=VOTRE_PRENOM&lastname=VOTRE_NOM&format=icalendar
    ```

5. Votre emploi du temps se mettra à jour automatiquement toutes les 6 heures.

## Mise en place

### Prérequis

- Python 3.8+
- Dépendances dans `requirements.txt`

### Installation

1. Cloner le répertoire et accéder au dossier cloné.
2. Créer un environnement virtuel : `python -m venv venv`
3. Activer l'environnement virtuel :
    - Windows : `.\venv\Scripts\activate`
    - Unix/MacOS : `source venv/bin/activate`
4. Installer les dépendances : `pip install -r requirements.txt`

### Exécution locale

Pour exécuter localement :

`uvicorn main:app --reload`


Le serveur démarrera et sera accessible sur `http://127.0.0.1:8000`.

## Collection API Bruno

Le fichier `.bruno` inclus dans ce répertoire contient une collection d'API prête à l'emploi pour le logiciel [Bruno](https://www.usebruno.com/). Il vous permet de tester facilement les différentes routes API disponibles.

### Comment utiliser la collection Bruno

1. Ouvrez le logiciel Bruno.
2. Allez dans le menu de gestion des collections.
3. Importez le fichier `.bruno` se trouvant dans ce répertoire.
4. Une fois importé, vous pourrez voir la liste des requêtes API disponibles et les tester directement.

Utiliser cette collection est un excellent moyen de comprendre rapidement comment interagir avec l'API et de vérifier son bon fonctionnement.

### Endpoints

- `/v1/month` : Retourne le fichier `.ics` de l'emploi du temps du mois en cours.
- `/v1/teams` : Retourne les liens Teams pour les cours en ligne.
- `/` : Vérification de l'état de santé du service.

## Architecture

L'architecture du projet est disponible dans `architecture.png`.

### `main.py`

- **Importations :** Utilise FastAPI pour la création de l'API, ainsi que les modules locaux pour la gestion des réponses et la logique métier.
- **Instance FastAPI :** Définit `app` comme une instance de FastAPI pour gérer les routes et les requêtes.
- **Routes API :**
   - `@app.get("/v1/month")` : Retourne l'emploi du temps du mois en format iCalendar.
   - `@app.get("/v1/teams")` : Retourne les liens Teams pour un cours spécifié.
   - `@app.get("/")` : Route de vérification de l'état de l'API.
- **Asynchronisme :** Les fonctions sont asynchrones pour une meilleure performance des requêtes.
- **Gestion des données :** Formatage des données reçues en réponse à des requêtes.

### `request.py`

- **Importations :** Modules pour la date/heure, requêtes HTTP, parsing HTML, création d'iCal, et gestion des variables d'environnement.
- **Fonctions :**
   - `async def get_current(firstname, lastname, format):` Scraps l'emploi du temps actuel sur 8 semaines.
   - `async def get_teams_link(firstname, lastname, date_time):` Obtient un lien Teams pour un cours spécifié.
   - `def parse_html_per_week(week_data, firstname, lastname):` Convertit le HTML scrapé en JSON structuré.
   - `def generate_ical(result):` Génère un fichier iCal à partir des données JSON.
- **Cache :** Utilisation d'un cache pour améliorer la performance des requêtes et limiter les appels redondants.
- **Gestion des erreurs :** Assure des réponses cohérentes même en cas d'erreur lors du scrapping.

Ce code facilite le scrapping des données de l'emploi du temps depuis le site de l'EPSI et leur conversion en fichiers iCal pour une intégration facile avec des calendriers tels que Google Calendar. La stratégie de requêtes concurrentes et la mise en cache des résultats sont employées pour une efficacité maximale.

## Contribution

N'hésitez pas à forker le projet et soumettre des pull requests ou créer des issues pour toute question ou suggestion d'amélioration.

---
Bonne continuation !


