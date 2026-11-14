from fastapi import FastAPI
from fastapi.responses import FileResponse
from app.config import settings
from app.routers.ws import router_ws
from fastapi import Depends
from app.database import get_db
from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text



app = FastAPI()
app.include_router(router_ws)


@app.get("/health/db")
async def get_health(db: Annotated[AsyncSession, Depends(get_db)]):
    await db.execute(text("SELECT 1"))
    return {'status': 'ok'}


@app.get('/')
async def get():
    return FileResponse("app/static/index.html")





        
