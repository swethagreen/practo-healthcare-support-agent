# src/practo_agent/memory.py

from langchain_core.chat_history import (
    InMemoryChatMessageHistory,
)
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import (
    RunnableWithMessageHistory,
)
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.runnables import RunnableLambda


# Separate histories for each conversation ID.
SESSION_HISTORIES = {}


def get_session_history(session_id: str):
    if session_id not in SESSION_HISTORIES:
        SESSION_HISTORIES[session_id] = (
            InMemoryChatMessageHistory()
        )

    return SESSION_HISTORIES[session_id]


def mock_conversation_response(inputs: dict) -> str:
    """A deterministic demonstration of contextual memory."""
    messages = inputs["messages"]

    current_question = next(
        message.content
        for message in reversed(messages)
        if isinstance(message, HumanMessage)
    )

    prior_human_messages = [
        message.content
        for message in messages[:-1]
        if isinstance(message, HumanMessage)
    ]

    if (
        "what specialty" in current_question.lower()
        and prior_human_messages
    ):
        return (
            "Your earlier message was: "
            f"{prior_human_messages[-1]}"
        )

    return f"You said: {current_question}"


prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        "You are a deterministic demonstration assistant. "
        "Use conversation history when relevant.",
    ),
    MessagesPlaceholder(variable_name="history"),
    ("human", "{question}"),
])

# The mock runnable consumes the assembled message history.
base_chain = RunnableLambda(
    lambda inputs: mock_conversation_response({
        "messages": inputs["history"] + [
            HumanMessage(content=inputs["question"])
        ]
    })
)

memory_chain = RunnableWithMessageHistory(
    base_chain,
    get_session_history,
    input_messages_key="question",
    history_messages_key="history",
)


def ask(question: str, session_id: str) -> str:
    result = memory_chain.invoke(
        {"question": question},
        config={"configurable": {"session_id": session_id}},
    )

    return result


if __name__ == "__main__":
    print("=== Session A ===")
    print(ask("I am asking about Cardiology.", "session-a"))
    print(ask("What specialty did I mention?", "session-a"))

    print("\n=== Fresh Session B ===")
    print(ask("What specialty did I mention?", "session-b"))
