from fastapi import FastAPI
from fastapi.responses import FileResponse

from app.routers.ws import router_ws


app = FastAPI()
app.include_router(router_ws)


@app.get('/')
async def get():
    return FileResponse("app/static/index.html")





        
