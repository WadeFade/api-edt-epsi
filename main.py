from fastapi import FastAPI

from request import get_current

app = FastAPI()

base_url: str = 'https://edtmobiliteng.wigorservices.net//WebPsDyn.aspx?action=posEDTBEECOME&serverid=i'


# https://calendar.lightin.io/v1/week?firstname=breval&lastname=lefloch


@app.get("/v1/month")
async def get_edt_month(firstname: str, lastname: str):
    # return await get_html_content(base_url, firstname, lastname, '2023-01-01')
    return await get_current(firstname, lastname)



