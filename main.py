import io
from datetime import datetime
from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from fastapi.responses import HTMLResponse

from request import get_current, get_teams_link

app = FastAPI()

base_url: str = 'https://edtmobiliteng.wigorservices.net//WebPsDyn.aspx?action=posEDTBEECOME&serverid=i'


@app.get("/v1/month")
async def get_edt_month(firstname: str, lastname: str, format: str = None):
    result = await get_current(firstname, lastname, format)
    data = result

    if format is None:
        return data

    # Créez un objet de fichier en mémoire en utilisant io.BytesIO()
    file = io.BytesIO()

    file.write(data.encode('utf-8'))

    # Renommez le fichier en mémoire en utilisant le nom souhaité
    file.seek(0)  # remettre le curseur au début du fichier
    file_name = f"edt_month-{str(datetime.now().timestamp()).replace('.', '')}.ics"

    headers = {"Content-Disposition": f"attachment; filename={file_name}"}
    return StreamingResponse(iter([file.getvalue()]), media_type="text/calendar", headers=headers)


@app.get("/v1/teams", response_class=HTMLResponse)
async def get_edt_teams(firstname: str, lastname: str, date_time: str):
    teams_link = await get_teams_link(firstname, lastname, date_time)
    # Crée un lien HTML pour la réunion Teams

    if teams_link or teams_link != "":
        link_html = f'<a href="{teams_link}" target="_blank">Join Teams Meeting</a>'
        return link_html

    # Gérer l'erreur et afficher un message approprié
    error_message = f"Les liens teams ne sont creer que 30 minutes avant les cours"
    return error_message

@app.get("/")
async def health_check():
    return {"status": "ok"}