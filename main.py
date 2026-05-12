from fastapi import FastAPI
from contextlib import asynccontextmanager

from database import create_db_and_tables
from routes_c import router as router_c


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield


app = FastAPI(
    title="Zadaća 2 - REST API",
    version="1.0.0",
    lifespan=lifespan
)

app.include_router(router_c, prefix="/student_c", tags=["Modul Korisnici i Rezervacije"])

@app.get("/")
def read_root():
    return {"message": "Zadaća 2 - REST API"}