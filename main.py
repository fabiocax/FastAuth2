
from fastapi import FastAPI 
from fastapi.openapi.utils import get_openapi
from oauth import main as auth
import uvicorn



app = FastAPI()
app.include_router(auth.oauth)

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="FastAuth2",
        version="2.5.0",
        description="",
        routes=app.routes,
    )
    openapi_schema["info"]["x-logo"] = {
        "url": "https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png"
    }
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi


@app.get("/")
async def root():
    return {"message": "FastAuth2"}
if __name__ == "__main__":
    #Calculator().createsuperuser('teste','teste')
    uvicorn.run("main:app", host="0.0.0.0", port=5000, log_level="info", debug=False)