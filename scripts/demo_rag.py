# scripts/demo_rag.py

import json
from pathlib import Path

from practo_agent.rag import PolicyRAG


PROJECT_ROOT = Path(__file__).resolve().parents[1]
REPORT_DIR = PROJECT_ROOT / "evaluation" / "reports"

DEMO_QUERIES = [
    "How far in advance should I cancel an appointment?",
    "What is the consultation fee for cardiology?",
    "What documents are needed for an insurance claim?",
    "How can I request a prescription refill?",
    "How long do laboratory results take?",
    "Who won the latest international football tournament?",
]


def main():
    calibration_path = (
        REPORT_DIR / "calibration_sentence.json"
    )

    if not calibration_path.exists():
        raise FileNotFoundError(
            "Run calibrate_threshold.py first."
        )

    calibration = json.loads(
        calibration_path.read_text(encoding="utf-8")
    )

    if not calibration["calibration_passed"]:
        raise RuntimeError(
            "Calibration failed. Do not use an "
            "uncalibrated similarity threshold."
        )

    threshold = calibration["threshold"]

    rag = PolicyRAG(
        strategy="sentence",
        threshold=threshold,
        top_k=5,
    )

    print(f"Calibrated threshold: {threshold:.4f}")

    for query in DEMO_QUERIES:
        result = rag.answer(query)

        print("\n" + "=" * 70)
        print("QUESTION:", query)
        print("ANSWER:", result["answer"])
        print("GROUNDED:", result["grounded"])
        print("REASON:", result["reason"])

        if result.get("top1_similarity") is not None:
            print(
                "TOP-1 SIMILARITY:",
                f'{result["top1_similarity"]:.4f}',
            )

        print(
            "EVIDENCE DOCUMENTS:",
            [
                item["document_id"]
                for item in result["evidence"]
            ],
        )


if __name__ == "__main__":
    main()