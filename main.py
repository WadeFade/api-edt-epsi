import io
import json

import redis
from datetime import datetime
from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from request import get_current

app = FastAPI()

base_url: str = 'https://edtmobiliteng.wigorservices.net//WebPsDyn.aspx?action=posEDTBEECOME&serverid=i'

# https://calendar.lightin.io/v1/week?firstname=breval&lastname=lefloch

r = redis.Redis(host='localhost', port=6379, decode_responses=True)


@app.get("/v1/month")
async def get_edt_month(firstname: str, lastname: str, format: str = None):
    # return await get_html_content(base_url, firstname, lastname, '2023-01-01')

    data = r.get(f"{firstname}.{lastname}")
    if data is None:
        result = await get_current(firstname, lastname, format)
        data = result
        r.set(f"{firstname}.{lastname}", json.dumps(data), ex=60 * 60 * 3)

    if format is None:
        return data

    # Créez un objet de fichier en mémoire en utilisant io.BytesIO()
    file = io.BytesIO()

    file.write(data.encode('utf-8'))

    # Renommez le fichier en mémoire en utilisant le nom souhaité
    file.seek(0)  # remettre le curseur au début du fichier
    file_name = f"edt_month-{str(datetime.now().timestamp()).replace('.', '')}.ics"

    # Utilisez la méthode StreamingResponse de FastAPI pour renvoyer le fichier renommé au client
    # Response.headers["Content-Disposition"] = f"attachment; filename={file_name}"

    headers = {"Content-Disposition": f"attachment; filename={file_name}"}
    return StreamingResponse(iter([file.getvalue()]), media_type="text/calendar", headers=headers)
# return Response(content=result, media_type="text/calendar")
