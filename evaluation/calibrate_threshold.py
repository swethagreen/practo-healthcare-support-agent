# evaluation/calibrate_threshold.py

import json
from pathlib import Path

from practo_agent.rag import PolicyRAG


PROJECT_ROOT = Path(__file__).resolve().parents[1]
REPORT_DIR = PROJECT_ROOT / "evaluation" / "reports"

CALIBRATION_CASES = [
    {
        "id": "C1",
        "query": "How far in advance should I cancel an appointment?",
        "in_scope": True,
    },
    {
        "id": "C2",
        "query": "What is the consultation fee for cardiology?",
        "in_scope": True,
    },
    {
        "id": "C3",
        "query": "What documents are needed for an insurance claim?",
        "in_scope": True,
    },
    {
        "id": "C4",
        "query": "How can I request a prescription refill?",
        "in_scope": True,
    },
    {
        "id": "C5",
        "query": "How long do laboratory results take?",
        "in_scope": True,
    },
    {
        "id": "C6",
        "query": "Who won the latest international football tournament?",
        "in_scope": False,
    },
    {
        "id": "C7",
        "query": "Explain how to build a rocket engine.",
        "in_scope": False,
    },
    {
        "id": "C8",
        "query": "What is the capital of Japan?",
        "in_scope": False,
    },
]


def calibrate(strategy: str):
    rag = PolicyRAG(
        strategy=strategy,
        threshold=None,
        top_k=5,
    )

    measurements = []

    for case in CALIBRATION_CASES:
        result = rag.retrieve(case["query"])

        row = {
            **case,
            "top1_similarity": result["top1_similarity"],
            "retrieved_documents": [
                item["parent_document_id"]
                for item in result["results"]
            ],
        }

        measurements.append(row)

        print(
            f'{case["id"]} | '
            f'{case["in_scope"]} | '
            f'{result["top1_similarity"]}'
        )

    in_scope = [
        row["top1_similarity"]
        for row in measurements
        if row["in_scope"]
        and row["top1_similarity"] is not None
    ]

    out_scope = [
        row["top1_similarity"]
        for row in measurements
        if not row["in_scope"]
        and row["top1_similarity"] is not None
    ]

    if not in_scope or not out_scope:
        raise RuntimeError(
            "Could not calculate both score groups."
        )

    max_out = max(out_scope)
    min_in = min(in_scope)

    # This experiment requires the observed groups to separate.
    # If they overlap, do not manufacture a threshold.
    if max_out >= min_in:
        report = {
            "strategy": strategy,
            "measurements": measurements,
            "max_out_of_scope_similarity": max_out,
            "min_in_scope_similarity": min_in,
            "threshold": None,
            "calibration_passed": False,
            "message": (
                "Score groups overlap. Improve retrieval or "
                "add a separate scope classifier, then rerun "
                "the experiment."
            ),
        }
    else:
        threshold = (max_out + min_in) / 2

        report = {
            "strategy": strategy,
            "measurements": measurements,
            "max_out_of_scope_similarity": max_out,
            "min_in_scope_similarity": min_in,
            "threshold": threshold,
            "calibration_passed": True,
            "message": (
                "Threshold selected between the observed "
                "out-of-scope and in-scope score ranges."
            ),
        }

    REPORT_DIR.mkdir(parents=True, exist_ok=True)

    output_file = REPORT_DIR / (
        f"calibration_{strategy}.json"
    )

    output_file.write_text(
        json.dumps(report, indent=2),
        encoding="utf-8",
    )

    print("\nCalibration summary")
    print(json.dumps(report, indent=2))
    print(f"\nSaved: {output_file}")

    return report


if __name__ == "__main__":
    for strategy in ("fixed", "sentence"):
        print(f"\n=== Strategy: {strategy} ===")
        calibrate(strategy)