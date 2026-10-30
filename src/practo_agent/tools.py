# src/practo_agent/tools.py

import json
import pathlib

import crewai.tools


PROJECT_ROOT = pathlib.Path(__file__).resolve().parents[2]
DATASET_PATH = PROJECT_ROOT / "data" / "appointments.json"

ESCALATION_THRESHOLD = 0.70


def load_appointments() -> dict:
    """Load the synthetic appointment dataset."""
    if not DATASET_PATH.exists():
        raise FileNotFoundError(
            f"Appointment dataset not found: {DATASET_PATH}. "
            "Run dataset.py first."
        )

    records = json.loads(
        DATASET_PATH.read_text(encoding="utf-8")
    )

    return {
        record["record_id"]: record
        for record in records
    }


def lookup_appointment(record_id: str) -> dict:
    """Look up one appointment and calculate its escalation score."""
    record_id = record_id.strip().upper()

    appointments = load_appointments()
    record = appointments.get(record_id)

    if record is None:
        return {
            "found": False,
            "record_id": record_id,
            "message": "Appointment record not found.",
        }

    follow_up = int(record["follow_up_required"])
    recency = record["days_since_created"] / 30.0

    escalation_score = round(
        0.6 * follow_up + 0.4 * recency,
        4,
    )

    return {
        "found": True,
        "record_id": record["record_id"],
        "category": record["category"],
        "status": record["status"],
        "consultation_fee_inr": record["consultation_fee_inr"],
        "days_since_created": record["days_since_created"],
        "follow_up_required": record["follow_up_required"],
        "escalation_score": escalation_score,
        "escalation_recommended": (
            escalation_score >= ESCALATION_THRESHOLD
        ),
    }


@crewai.tools.tool("check_appointment_status")
def check_appointment_status(record_id: str) -> dict:
    """Look up a synthetic appointment using its record ID.

    Returns its status, consultation fee in INR, and a designed
    escalation score. Use this tool when a patient asks about a
    specific appointment and provides an appointment record ID.
    Do not invent appointment records or statuses.
    """
    return lookup_appointment(record_id)


# validating the code testing
def report_escalation_distribution():
    print("Testing started.")
    appointments = load_appointments()
    records = list(appointments.values())

    scores = []

    for record in records:
        follow_up = int(record["follow_up_required"])
        recency = record["days_since_created"] / 30.0

        score = 0.6 * follow_up + 0.4 * recency
        scores.append(score)

    flagged = sum(
        score >= ESCALATION_THRESHOLD
        for score in scores
    )

    print(f"Records evaluated: {len(scores)}")
    print(f"Escalation threshold: {ESCALATION_THRESHOLD}")
    print(f"Records flagged: {flagged}")
    print(
        f"Flagged percentage: "
        f"{100 * flagged / len(scores):.2f}%"
    )

    print(
        "Days-since-created 80th percentile:",
        sorted(
            r["days_since_created"] for r in records
        )[int(0.8 * (len(records) - 1))],
    )

print(report_escalation_distribution())
## initial testing done

import practo_agent.rag


@crewai.tools.tool("rag_lookup")
def rag_lookup(query: str) -> str:
    """Retrieve policy evidence from the Practo knowledge base.

    Use for questions about booking, cancellation, fees, insurance,
    prescriptions, laboratory results, telemedicine, privacy,
    follow-ups, second opinions, and home visits.
    Do not use this tool to determine a specific appointment's
    current status.
    """
    rag = practo_agent.rag.PolicyRAG(
        strategy="fixed",
        threshold=None,
        top_k=5,
    )

    result = rag.retrieve(query)

    return json.dumps(
        result,
        ensure_ascii=False,
    )