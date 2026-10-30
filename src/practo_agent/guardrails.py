# src/practo_agent/guardrails.py

import re
from dataclasses import dataclass


# Demonstration pattern for Indian-style 10-digit mobile numbers.
# Supports an optional +91 or 91 prefix.
PHONE_PATTERN = re.compile(
    r"(?<!\d)(?:\+91[\s-]?|91[\s-]?|0)?"
    r"[6-9]\d{9}(?!\d)"
)

INJECTION_PATTERNS = [
    re.compile(
        r"ignore\s+(all\s+)?previous\s+instructions",
        re.IGNORECASE,
    ),
    re.compile(
        r"reveal\s+(the\s+)?system\s+prompt",
        re.IGNORECASE,
    ),
    re.compile(
        r"bypass\s+(all\s+)?safety",
        re.IGNORECASE,
    ),
    re.compile(
        r"ignore\s+your\s+guardrails",
        re.IGNORECASE,
    ),
]


@dataclass
class GuardrailResult:
    allowed: bool
    sanitized_input: str
    reason: str
    pii_masked: bool = False


def mask_phone_numbers(text: str) -> tuple[str, bool]:
    """Mask matching phone numbers in the input."""
    masked_text, count = PHONE_PATTERN.subn(
        "[PHONE_MASKED]",
        text,
    )

    return masked_text, count > 0


def detect_prompt_injection(text: str) -> bool:
    """Detect a small set of known injection patterns."""
    return any(
        pattern.search(text)
        for pattern in INJECTION_PATTERNS
    )


def validate_input(text: str) -> GuardrailResult:
    """Mask phone numbers and reject detected prompt injection."""
    if not isinstance(text, str) or not text.strip():
        return GuardrailResult(
            allowed=False,
            sanitized_input="",
            reason="empty_or_invalid_input",
        )

    sanitized, pii_masked = mask_phone_numbers(text)

    if detect_prompt_injection(sanitized):
        return GuardrailResult(
            allowed=False,
            sanitized_input=sanitized,
            reason="prompt_injection_detected",
            pii_masked=pii_masked,
        )

    return GuardrailResult(
        allowed=True,
        sanitized_input=sanitized,
        reason="input_accepted",
        pii_masked=pii_masked,
    )


def groundedness_check(
    answer: str,
    retrieved_contexts: list[str],
    *,
    minimum_overlap: float = 0.5,
) -> dict:
    """A conservative lexical support check for MOCK_LLM.

    This is a lightweight heuristic, not a semantic proof of
    groundedness. It requires a minimum proportion of the answer's
    meaningful tokens to occur in the retrieved context.
    """
    if not answer.strip() or not retrieved_contexts:
        return {
            "allowed": False,
            "reason": "missing_answer_or_evidence",
            "overlap": 0.0,
        }

    def tokens(text):
        return {
            token.lower()
            for token in re.findall(r"\b[a-zA-Z0-9]+\b", text)
            if len(token) > 2
        }

    answer_tokens = tokens(answer)
    context_tokens = tokens(" ".join(retrieved_contexts))

    if not answer_tokens:
        return {
            "allowed": False,
            "reason": "no_meaningful_answer_tokens",
            "overlap": 0.0,
        }

    overlap = (
        len(answer_tokens & context_tokens)
        / len(answer_tokens)
    )

    allowed = overlap >= minimum_overlap

    return {
        "allowed": allowed,
        "reason": (
            "context_supports_answer"
            if allowed
            else "insufficient_context_support"
        ),
        "overlap": round(overlap, 4),
    }


def apply_output_guardrail(
    answer: str,
    retrieved_contexts: list[str],
) -> dict:
    result = groundedness_check(
        answer,
        retrieved_contexts,
    )

    if not result["allowed"]:
        return {
            **result,
            "answer": (
                "I don't know based on the available "
                "policy documents. Please contact the clinic "
                "for further assistance."
            ),
            "refused": True,
        }

    return {
        **result,
        "answer": answer,
        "refused": False,
    }

