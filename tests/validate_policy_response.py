from practo_agent.schemas import PractoResponse
from practo_agent.guardrails import apply_output_guardrail


def validate_policy_response(
    draft: str,
    evidence: list[dict],
) -> PractoResponse:
    contexts = [
        item["text"]
        for item in evidence
    ]

    check = apply_output_guardrail(
        draft,
        contexts,
    )

    return PractoResponse.model_validate({
        "response": check["answer"],
        "intent": (
            "refusal"
            if check["refused"]
            else "policy_question"
        ),
        "grounded": check["allowed"],
        "refused": check["refused"],
        "evidence": [
            {
                "source_id": item["source_id"],
                "text": item["text"],
            }
            for item in evidence
        ] if check["allowed"] else [],
    })