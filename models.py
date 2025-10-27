from pydantic import BaseModel, Field
from typing import List, Optional, Literal

class Vehicle(BaseModel):
    make: Optional[str] = None
    model: Optional[str] = None
    year_jp: Optional[str] = None
    year: Optional[int] = None
    color: Optional[str] = None
    price: Optional[str] = None

class CaseCreate(BaseModel):
    vehicle: Vehicle
    raw_inquiry: str
    customer_name: Optional[str] = None

class QAItem(BaseModel):
    key: str
    question: str
    answer: Optional[str] = None
    status: Literal["answered","unconfirmed","skipped"] = "answered"

class GenerateRequest(BaseModel):
    qa_items: List[QAItem]
    tone: Optional[Literal["誠実","上質","フレンドリー","簡潔"]] = "誠実"
    closing_variant: Optional[str] = None
    future_style: Optional[Literal["open_sport","luxury_sedan","suv","ev","compact"]] = None
    signature_block: Optional[str] = None
