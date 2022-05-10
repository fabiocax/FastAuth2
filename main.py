
from fastapi import FastAPI 
from oauth import main as auth
import uvicorn
from cli import Calculator


app = FastAPI()
app.include_router(auth.oauth)

@app.get("/")
async def root():
    return {"message": "FastAuth2"}
if __name__ == "__main__":
    #Calculator().createsuperuser('teste','teste')
    uvicorn.run("main:app", host="0.0.0.0", port=5000, log_level="info", debug=False)