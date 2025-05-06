from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, Path, Request
from pydantic import BaseModel
from starlette import status
from torch.distributed.nn.jit import templates

from database import SessionLocal
from typing import Annotated
from sqlalchemy.orm import Session

from models import MoodLogs
from routers.auth import get_current_user

router = APIRouter(
    prefix="/mood_logs",
    tags=["Mood Logs"],
)


class MoodLog(BaseModel):
    user_id: int
    mood_text: str
    created_at: datetime


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]

@router.post("/create_mood_log", status_code=status.HTTP_201_CREATED)
async def create_mood_log(mood_log: MoodLog, user: user_dependency, db: db_dependency):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")

    mood_log_data = MoodLogs(
        user_id=user.get('id'),
        mood_text=mood_log.mood_text,
        created_at=datetime.now()
    )
    db.add(mood_log_data)
    db.commit()


@router.get("/get_all_mood_logs", status_code=status.HTTP_200_OK)
async def read_all_mood_logs(user: user_dependency, db: db_dependency):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
    return db.query(MoodLogs).filter(MoodLogs.user_id == user.get('id')).all()


@router.get("/get_by_id/{user_id}", status_code=status.HTTP_200_OK)
async def read_by_id(user: user_dependency, db: db_dependency, user_id: int = Path(gt=0)):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")

    mood_logs = db.query(MoodLogs).filter(MoodLogs.user_id == user_id).first()
    if mood_logs is not None:
        return mood_logs
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Mood logs not found")
