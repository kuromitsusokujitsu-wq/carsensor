from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from models import CaseCreate, GenerateRequest
from services.openai_client import extract_questions, compose_reply

app = FastAPI(title="CarSensor Reply MVP")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.post("/cases")
def create_case(body: CaseCreate):
    questions = extract_questions(body.vehicle.model_dump(), body.raw_inquiry)
    return {"initial_questions": questions}

@app.post("/cases/generate")
def generate_reply(body: GenerateRequest):
    qa_dump = [q.model_dump() for q in body.qa_items]
    payload = {
        "qa_items": qa_dump,
        "tone": body.tone,
        "closing_variant": body.closing_variant,
        "future_style": body.future_style,
        "signature_block": body.signature_block,
    }
    text = compose_reply(payload)
    return {"draft_text": text}

@app.get("/health")
def health():
    return {"status": "ok"}
