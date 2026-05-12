from fastapi import FastAPI
from contextlib import asynccontextmanager
from database import create_db_and_tables, get_session
from routes_a import router as router_a
from routes_b import router as router_b
from routes_c import router as router_c
from seed_database import seed_all_tables


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Kreiranje tabela i punjenje početnim podacima
    # FastAPI dependency_overrides koristi originalni callable kao ključ (npr. get_session u testovima)
    if get_session not in app.dependency_overrides:
        create_db_and_tables()
        seed_all_tables()
    yield


app = FastAPI(
    title="Zadaća 2 - REST API",
    version="1.0.0",
    lifespan=lifespan
)


@app.get("/")
def read_root():
    return {"message": "Zadaća 2 - REST API"}

app.include_router(router_users)

app.include_router(router_a)
app.include_router(router_b)
app.include_router(router_c, prefix="/student_c", tags=["Modul Korisnici i Rezervacije"])