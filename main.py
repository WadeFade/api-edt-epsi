import io
from datetime import datetime

from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from request import get_current

app = FastAPI()

base_url: str = 'https://edtmobiliteng.wigorservices.net//WebPsDyn.aspx?action=posEDTBEECOME&serverid=i'


# https://calendar.lightin.io/v1/week?firstname=breval&lastname=lefloch


@app.get("/v1/month")
async def get_edt_month(firstname: str, lastname: str, format: str = None):
    # return await get_html_content(base_url, firstname, lastname, '2023-01-01')
    result = await get_current(firstname, lastname, format)

    if format is None:
        return result

    # Créez un objet de fichier en mémoire en utilisant io.BytesIO()
    file = io.BytesIO()

    file.write(result.encode('utf-8'))

    # Renommez le fichier en mémoire en utilisant le nom souhaité
    file.seek(0)  # remettre le curseur au début du fichier
    file_name = f"edt_month-{str(datetime.now().timestamp()).replace('.', '')}.ics"

    # Utilisez la méthode StreamingResponse de FastAPI pour renvoyer le fichier renommé au client
    # Response.headers["Content-Disposition"] = f"attachment; filename={file_name}"

    headers = {"Content-Disposition": f"attachment; filename={file_name}"}
    return StreamingResponse(iter([file.getvalue()]), media_type="text/calendar", headers=headers)
# return Response(content=result, media_type="text/calendar")
