from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from sqlmodel import SQLModel
from app.core.database import engine
from app.api import auth, activities, stats

@asynccontextmanager
async def lifespan(app: FastAPI):
    SQLModel.metadata.create_all(engine)
    yield
    engine.dispose()

app = FastAPI(
    title="KairoFlow API",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/auth")
app.include_router(activities.router, prefix="/activities", tags=["activities"])
app.include_router(stats.router, prefix="/stats", tags=["statistics"])

@app.get("/")
def read_root():
    return {"message": "KairoFlow API is running"}