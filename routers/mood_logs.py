from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, Path
from pydantic import BaseModel
from starlette import status

from database import SessionLocal
from typing import Annotated
from sqlalchemy.orm import Session

from models import MoodLogs
from routers.auth import get_current_user

router = APIRouter(
    prefix="/mood_logs",
    tags=["mood_logs"],
)


class MoodLog(BaseModel):
    user_id: int
    mood_text: str
    date: str
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

    try:
        date_value = datetime.strptime(mood_log.date, "%Y-%m-%d").date()  # String'i date objesine dönüştür
    except ValueError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid date format")

    mood_log_data = MoodLogs(
        user_id=user.get('id'),
        mood_text=mood_log.mood_text,
        date=date_value,
        created_at=datetime.now()
    )
    db.add(mood_log_data)
    db.commit()
    db.refresh(mood_log_data)
    return mood_log_data


@router.get("/get_all_mood_logs", status_code=status.HTTP_200_OK)
async def get_all_mood_logs(user: user_dependency, db: db_dependency):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
    return db.query(MoodLogs).filter(MoodLogs.user_id == user.get('id')).all()


@router.get("/mood_logs/{user_id}", status_code=status.HTTP_200_OK)
async def get_by_id(user: user_dependency, db: db_dependency, user_id: int = Path(gt=0)):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")

    # Sadece kendi loglarını görüntüleyebilir kontrolü
    if user.get('id') != user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Cannot access other users' logs")

    mood_logs = db.query(MoodLogs).filter(MoodLogs.user_id == user_id).all()
    if mood_logs:
        return mood_logs
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Mood logs not found")
