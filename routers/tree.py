from datetime import date, datetime
from pydantic import BaseModel
from fastapi import APIRouter, Depends, HTTPException
from models import TreeState, User
from database import SessionLocal
from typing import Annotated
from sqlalchemy.orm import Session
from routers.mood import analyze_mood
from routers.tree_utils import map_emotion_to_tree
from routers.auth import get_current_user

router = APIRouter(
    prefix="/tree",
    tags=["Tree Analysis"],
)


class TreeStateSchema(BaseModel):
    date: date
    emotion: str
    leaf_color: str
    has_flowers: bool
    falling_leaves: bool
    created_at: datetime


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]


@router.get("/today")
def get_today_tree(db: db_dependency, user: User = Depends(get_current_user)):
    today = date.today()
    tree = db.query(TreeState).filter_by(user_id=user.id, date=today).first()
    if not tree:
        raise HTTPException(status_code=404, detail="No tree state for today")
    return tree


@router.post("/create")
def create_tree_state(tree_state: TreeStateSchema, db: db_dependency, user: User = Depends(get_current_user)):
    today = date.today()
    existing_tree = db.query(TreeState).filter_by(user_id=user.id, date=today).first()

    if existing_tree:
        raise HTTPException(status_code=400, detail="Tree state for today already exists")

    new_tree = TreeState(
        user_id=user.id,
        date=today,
        emotion=tree_state.emotion,
        leaf_color=tree_state.leaf_color,
        has_flowers=tree_state.has_flowers,
        falling_leaves=tree_state.falling_leaves
    )

    db.add(new_tree)
    db.commit()
    db.refresh(new_tree)

    return new_tree


class MoodTextInput(BaseModel):
    text: str


@router.post("/from-mood")
def create_tree_from_mood(
        data: MoodTextInput,
        db: Session = Depends(get_db),
        user: dict = Depends(get_current_user)
):
    today = date.today()

    # Aynı güne iki giriş yapılmasın
    existing = db.query(TreeState).filter_by(user_id=user.id, date=today).first()
    if existing:
        raise HTTPException(status_code=400, detail="Mood already submitted for today.")

    # 1. Duygu analizi
    result = analyze_mood(data.text)
    emotion = result["dominant_emotion"]
    score = result["sentiment_score"]

    # 2. Ağaç durumu eşle
    tree_state = map_emotion_to_tree(emotion)

    # 3. Veritabanına yaz
    new_state = TreeState(
        user_id=user.id,
        date=today,
        emotion=emotion,
        leaf_color=tree_state["leaf_color"],
        has_flowers=tree_state["has_flowers"],
        falling_leaves=tree_state["falling_leaves"],
        created_at=datetime.utcnow()
    )
    db.add(new_state)
    db.commit()

    return {
        "message": "Tree updated based on mood.",
        "tree_state": {
            "emotion": emotion,
            "leaf_color": tree_state["leaf_color"],
            "has_flowers": tree_state["has_flowers"],
            "falling_leaves": tree_state["falling_leaves"]
        },
        "mood_analysis": result["details"]
    }
