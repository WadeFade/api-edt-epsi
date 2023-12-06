import io
from datetime import datetime
from fastapi import FastAPI
from fastapi.responses import StreamingResponse
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


@app.get("/v1/teams")
async def get_edt_teams(firstname: str, lastname: str, date_time: str):
    result = await get_teams_link(firstname, lastname, date_time)
    return f"{firstname} {lastname} {date_time}: {result}"
