# dataset.py

import json
import random
from collections import Counter
from pathlib import Path

SEED = 42
NUM_RECORDS = 50

CATEGORIES = [
    "General Medicine",
    "Cardiology",
    "Dermatology",
    "Pediatrics",
    "Orthopedics",
]

STATUSES = [
    "Scheduled",
    "Completed",
    "Cancelled",
    "No-Show",
    "Rescheduled",
]

CATEGORY_WEIGHTS = [30, 15, 15, 20, 20]
STATUS_WEIGHTS = [35, 35, 10, 5, 15]

# Follow-up probability is 20%.
FOLLOW_UP_PROBABILITY = 0.20

# INR 500–2500 covers a plausible range of outpatient
# consultation fees for this synthetic multi-specialty dataset.
FEE_RANGE_INR = (500, 2500)


def generate_appointments():
    rng = random.Random(SEED)
    records = []

    for i in range(1, NUM_RECORDS + 1):
        record = {
            "record_id": f"APT{i:04d}",
            "category": rng.choices(
                CATEGORIES, weights=CATEGORY_WEIGHTS, k=1
            )[0],
            "status": rng.choices(
                STATUSES, weights=STATUS_WEIGHTS, k=1
            )[0],
            "consultation_fee_inr": rng.randint(*FEE_RANGE_INR),
            "days_since_created": rng.randint(0, 30),
            "follow_up_required": (
                rng.random() < FOLLOW_UP_PROBABILITY
            ),
        }

        records.append(record)

    return records


def validate_appointments(records):
    assert len(records) >= 40

    ids = [r["record_id"] for r in records]
    assert len(ids) == len(set(ids)), "Duplicate record IDs"

    assert set(CATEGORIES).issubset(
        {r["category"] for r in records}
    )

    assert set(STATUSES).issubset(
        {r["status"] for r in records}
    )

    for record in records:
        assert FEE_RANGE_INR[0] <= record[
            "consultation_fee_inr"
        ] <= FEE_RANGE_INR[1]

        assert 0 <= record["days_since_created"] <= 30
        assert isinstance(record["follow_up_required"], bool)

    category_counts = Counter(
        r["category"] for r in records
    )
    status_counts = Counter(
        r["status"] for r in records
    )

    for category in CATEGORIES:
        assert category_counts[category] >= 3, (
            f"Insufficient records for {category}"
        )

    for status in STATUSES:
        assert status_counts[status] >= 1, (
            f"Missing status: {status}"
        )

    follow_up_count = sum(
        r["follow_up_required"] for r in records
    )
    follow_up_percentage = (
        follow_up_count / len(records)
    ) * 100

    assert 10 <= follow_up_percentage <= 30, (
        f"Follow-up rate is {follow_up_percentage:.2f}%. "
        "Choose a new seed or adjust the generation weights."
    )

    return category_counts, status_counts, follow_up_percentage


def main():
    records = generate_appointments()

    categories, statuses, follow_up_pct = (
        validate_appointments(records)
    )

    output_path = Path("data/appointments.json")
    output_path.parent.mkdir(parents=True, exist_ok=True)

    output_path.write_text(
        json.dumps(records, indent=2),
        encoding="utf-8",
    )

    print(f"Seed: {SEED}")
    print(f"Total appointments: {len(records)}")
    print(f"Consultation fee range: {FEE_RANGE_INR}")

    print("\nCategory counts:")
    for category in CATEGORIES:
        print(f"  {category}: {categories[category]}")

    print("\nStatus counts:")
    for status in STATUSES:
        print(f"  {status}: {statuses[status]}")

    print(
        f"\nFollow-up required: "
        f"{sum(r['follow_up_required'] for r in records)}"
        f"/{len(records)} ({follow_up_pct:.2f}%)"
    )

    print(f"\nDataset saved to {output_path}")


if __name__ == "__main__":
    main()