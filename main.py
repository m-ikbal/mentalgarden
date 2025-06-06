from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routers.auth import router as auth_router
from routers.mood import router as mood_router
from routers.tree import router as tree_router
from routers.mood_logs import router as mood_logs_router
from models import Base
from database import engine

app = FastAPI()
app.include_router(auth_router)
app.include_router(mood_router)
app.include_router(tree_router)
app.include_router(mood_logs_router)

Base.metadata.create_all(bind=engine)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # veya ["http://localhost:3000"] gibi özelleştirebilirsin
    allow_credentials=True,
    allow_methods=["*"],  # ["POST", "GET", "OPTIONS"] olarak da sınırlandırabilirsin
    allow_headers=["*"],
)