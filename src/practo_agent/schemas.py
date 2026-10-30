
# src/practo_agent/schemas.py

from typing import Literal

from pydantic import BaseModel, Field


class Evidence(BaseModel):
    source_id: str
    text: str


class PractoResponse(BaseModel):
    response: str = Field(
        min_length=1,
        description="The final patient-facing answer.",
    )

    intent: Literal[
        "policy_question",
        "appointment_lookup",
        "general",
        "refusal",
    ]

    status: str | None = None
    consultation_fee_inr: int | None = None

    escalation_score: float | None = Field(
        default=None,
        ge=0.0,
        le=1.0,
    )

    escalation_recommended: bool = False

    grounded: bool

    refused: bool = False

    evidence: list[Evidence] = Field(
        default_factory=list
    )

#Validate outputs
from practo_agent.schemas import PractoResponse

payload = {
    "response": "Your appointment is scheduled.",
    "intent": "appointment_lookup",
    "status": "Scheduled",
    "consultation_fee_inr": 1200,
    "escalation_score": 0.2,
    "escalation_recommended": False,
    "grounded": True,
    "refused": False,
    "evidence": [],
}

validated = PractoResponse.model_validate(payload)

print(validated.model_dump())