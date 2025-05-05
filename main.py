from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from routers.auth import router as auth_router
from routers.mood import router as mood_router
from models import Base
from database import engine

app = FastAPI()
app.include_router(auth_router)
app.include_router(mood_router)


Base.metadata.create_all(bind=engine)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # veya ["http://localhost:3000"] gibi özelleştirebilirsin
    allow_credentials=True,
    allow_methods=["*"],  # ["POST", "GET", "OPTIONS"] olarak da sınırlandırabilirsin
    allow_headers=["*"],
)
