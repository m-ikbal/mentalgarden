from transformers import AutoTokenizer, AutoModelForSequenceClassification, pipeline
import torch
from fastapi import APIRouter
from pydantic import BaseModel
import torch.nn.functional as F

router = APIRouter(
    prefix="/mood",
    tags=["Mood Analysis"],
)

model_name = "j-hartmann/emotion-english-distilroberta-base"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSequenceClassification.from_pretrained(model_name)


class MoodInput(BaseModel):
    text: str


@router.post("/analyze-mood")
async def analyze_mood(data: MoodInput):
    inputs = tokenizer(data.text, return_tensors="pt")
    outputs = model(**inputs)
    probs = F.softmax(outputs.logits, dim=1)
    labels = model.config.id2label

    scores = probs[0].tolist()
    result = [{"label": labels[i], "score": round(score, 3)} for i, score in enumerate(scores)]
    result.sort(key=lambda x: x["score"], reverse=True)

    EMOTION_SCORE = {
        "joy": 2, "love": 2, "neutral": 0,
        "sadness": -1, "fear": -2, "anger": -2,
        "surprise": 0
    }

    top_emotion = result[0]["label"]
    mood_score = EMOTION_SCORE.get(top_emotion, 0)

    return {
        "dominant_emotion": top_emotion,
        "score": result[0]["score"],  # modelin confidence değeri
        "sentiment_score": mood_score,  # kendi manuel skorun
        "details": result[:3]
    }
