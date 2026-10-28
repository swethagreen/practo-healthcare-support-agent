import re


def sentence_chunks(
    text: str,
    max_chars: int = 500,
):
    sentences = re.split(
        r"(?<=[.!?])\s+",
        text.strip(),
    )

    chunks = []
    current = ""

    for sentence in sentences:
        sentence = sentence.strip()

        if not sentence:
            continue

        if current and len(current) + len(sentence) + 1 > max_chars:
            chunks.append(current)
            current = sentence
        else:
            current = (
                f"{current} {sentence}".strip()
            )

    if current:
        chunks.append(current)

    return chunks