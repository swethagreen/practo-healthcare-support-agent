# evaluation/evaluate_chunking.py

import json
from pathlib import Path

from practo_agent.rag import PolicyRAG


PROJECT_ROOT = Path(__file__).resolve().parents[1]
REPORT_DIR = PROJECT_ROOT / "evaluation" / "reports"

# Expected relevant documents are defined before retrieval.
# IDs correspond to the policy filenames without ".txt".
EVALUATION_CASES = [
    {
        "id": "Q1",
        "query": "How far in advance should I cancel an appointment?",
        "expected_documents": {
            "cancellation_rescheduling"
        },
    },
    {
        "id": "Q2",
        "query": "What is the consultation fee for cardiology?",
        "expected_documents": {
            "consultation_fees"
        },
    },
    {
        "id": "Q3",
        "query": "What documents are needed for an insurance claim?",
        "expected_documents": {
            "insurance_claims"
        },
    },
    {
        "id": "Q4",
        "query": "How can I request a prescription refill?",
        "expected_documents": {
            "prescription_refills"
        },
    },
    {
        "id": "Q5",
        "query": "How long do laboratory results take?",
        "expected_documents": {
            "lab_turnaround"
        },
    },
]


def evaluate_query(rag, case):
    result = rag.retrieve(case["query"])

    # Map retrieved chunks to unique parent documents.
    retrieved_documents = list(dict.fromkeys(
        item["parent_document_id"]
        for item in result["results"]
    ))

    expected = set(case["expected_documents"])
    retrieved = set(retrieved_documents)

    relevant_retrieved = expected & retrieved

    precision = (
        len(relevant_retrieved) / len(retrieved)
        if retrieved else 0.0
    )

    recall = (
        len(relevant_retrieved) / len(expected)
        if expected else 0.0
    )

    return {
        "query_id": case["id"],
        "query": case["query"],
        "expected_documents": sorted(expected),
        "retrieved_documents": retrieved_documents,
        "relevant_retrieved_documents": sorted(
            relevant_retrieved
        ),
        "precision_numerator": len(relevant_retrieved),
        "precision_denominator": len(retrieved),
        "precision": precision,
        "recall_numerator": len(relevant_retrieved),
        "recall_denominator": len(expected),
        "recall": recall,
        "top1_similarity": result["top1_similarity"],
    }


def evaluate_strategy(strategy):
    rag = PolicyRAG(
        strategy=strategy,
        threshold=None,
        top_k=5,
    )

    rows = [
        evaluate_query(rag, case)
        for case in EVALUATION_CASES
    ]

    mean_precision = sum(
        row["precision"] for row in rows
    ) / len(rows)

    mean_recall = sum(
        row["recall"] for row in rows
    ) / len(rows)

    return {
        "strategy": strategy,
        "top_k": rag.top_k,
        "queries_evaluated": len(rows),
        "results": rows,
        "mean_precision": mean_precision,
        "mean_recall": mean_recall,
    }


def main():
    REPORT_DIR.mkdir(parents=True, exist_ok=True)

    reports = {}

    for strategy in ("fixed", "sentence"):
        report = evaluate_strategy(strategy)
        reports[strategy] = report

        output_file = REPORT_DIR / (
            f"chunking_{strategy}.json"
        )

        output_file.write_text(
            json.dumps(report, indent=2),
            encoding="utf-8",
        )

        print(f"\n=== {strategy.upper()} ===")

        for row in report["results"]:
            print(f'\n{row["query_id"]}: {row["query"]}')
            print(
                f'Expected: {row["expected_documents"]}'
            )
            print(
                f'Retrieved: {row["retrieved_documents"]}'
            )
            print(
                f'Precision = '
                f'{row["precision_numerator"]}/'
                f'{row["precision_denominator"]} '
                f'= {row["precision"]:.3f}'
            )
            print(
                f'Recall = '
                f'{row["recall_numerator"]}/'
                f'{row["recall_denominator"]} '
                f'= {row["recall"]:.3f}'
            )

        print(
            f'\nMean precision: '
            f'{report["mean_precision"]:.3f}'
        )
        print(
            f'Mean recall: {report["mean_recall"]:.3f}'
        )
        print(f"Saved: {output_file}")

    comparison = {
        "fixed": {
            "mean_precision": reports["fixed"]["mean_precision"],
            "mean_recall": reports["fixed"]["mean_recall"],
        },
        "sentence": {
            "mean_precision": reports["sentence"]["mean_precision"],
            "mean_recall": reports["sentence"]["mean_recall"],
        },
    }

    comparison_file = (
        REPORT_DIR / "chunking_comparison.json"
    )

    comparison_file.write_text(
        json.dumps(comparison, indent=2),
        encoding="utf-8",
    )

    print("\n=== FINAL COMPARISON ===")
    print(json.dumps(comparison, indent=2))


if __name__ == "__main__":
    main()