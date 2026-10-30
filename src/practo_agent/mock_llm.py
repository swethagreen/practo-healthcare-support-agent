from typing import Any

from crewai.llms.base_llm import BaseLLM


class MockLLM(BaseLLM):
    model: str = "practo-deterministic-mock"

    def __init__(self, **data: Any) -> None:
        data.setdefault("model", "practo-deterministic-mock")
        super().__init__(**data)

    def call(self, messages: Any, **kwargs: Any) -> str:
        return (
            "Final Answer: Deterministic mock response. "
            "No external language model was called."
        )