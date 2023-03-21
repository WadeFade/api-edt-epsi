from fastapi import FastAPI

app = FastAPI()


# https://calendar.lightin.io/v1/week?firstname=breval&lastname=lefloch
@app.get("/v1/month")
async def get_edt_month(firstname: str, lastname: str):
    return {"firstname": firstname, "lastname": lastname}
