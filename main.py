from fastapi import FastAPI
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from cachetools import TTLCache
from datetime import datetime, timedelta
import asyncio

# Importez vos modules personnalisés ici
from request import get_current, get_teams_link

app = FastAPI()

# Configuration du cache et de l'ordonnanceur
cache = TTLCache(maxsize=1000, ttl=1800)  # TTL de 30 minutes
scheduler = AsyncIOScheduler()
scheduler.start()

# Ensemble pour suivre les cours déjà planifiés
scheduled_courses = set()


async def cache_teams_link(firstname, lastname, course_id):
    datetime_str = course_id.split('_')[-1]
    link = await get_teams_link(firstname, lastname, datetime_str)
    if link:
        cache[course_id] = link


async def schedule_course(firstname, lastname, course):
    course_id = f"{firstname}_{lastname}_{course['date']}_{course['start']}"
    if course_id not in scheduled_courses:
        schedule_time = datetime.strptime(f"{course['date']} {course['start']}", "%d/%m/%Y %H:%M") - timedelta(
            minutes=30)
        scheduler.add_job(cache_teams_link, 'date', run_date=schedule_time, args=[firstname, lastname, course_id])
        scheduled_courses.add(course_id)


@app.get("/v1/month")
async def get_edt_month(firstname: str, lastname: str, format: str = None):
    result = await get_current(firstname, lastname, format)

    print("Résultat de get_current:", result)  # Log pour débogage

    # Assurez-vous que result est une liste de dictionnaires
    # for week in result:
    #     print("Semaine:", week)  # Log pour débogage
    #
    #     if isinstance(week, dict):  # Vérifiez si week est un dictionnaire
    #         for day, courses in week.items():
    #             for course in courses:
    #                 if "distanciel" in course['description'].lower():
    #                     await schedule_course(firstname, lastname, course)
    #     else:
    #         print("Erreur: week n'est pas un dictionnaire")  # Log d'erreur

    return result


@app.get("/v1/teams")
async def get_edt_teams(firstname: str, lastname: str, date_time: str):
    course_id = f"{firstname}_{lastname}_{date_time}"
    cached_link = cache.get(course_id)
    if cached_link:
        return cached_link
    else:
        return await get_teams_link(firstname, lastname, date_time)


# Autres routes et logique FastAPI si nécessaire...

# Point d'entrée pour l'application FastAPI
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
