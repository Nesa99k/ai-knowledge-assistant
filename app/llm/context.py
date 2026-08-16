import re


def format_table(text: str) -> str:
    """Convert a Markdown-style table into a clearer LLM-readable format."""

    lines = [
        line.strip()
        for line in text.splitlines()
        if line.strip()
    ]

    table_lines = [
        line
        for line in lines
        if line.startswith("|") and line.endswith("|")
    ]

    if len(table_lines) < 2:
        return text

    header = [
        cell.strip()
        for cell in table_lines[0].strip("|").split("|")
    ]

    # Skip markdown separator row
    data_lines = [
        line
        for line in table_lines[1:]
        if not re.fullmatch(
            r"\|?\s*:?-+:?\s*(\|\s*:?-+:?\s*)+\|?",
            line,
        )
    ]

    formatted_rows = []

    for line in data_lines:
        cells = [
            cell.strip()
            for cell in line.strip("|").split("|")
        ]

        if not cells:
            continue

        row_name = cells[0]

        row_parts = [
            f"{header[i]}: {cells[i]}"
            for i in range(1, min(len(header), len(cells)))
            if cells[i]
        ]

        formatted_rows.append(
            f"{row_name}\n"
            + "\n".join(
                f"- {part}"
                for part in row_parts
            )
        )

    if not formatted_rows:
        return text

    return "\n\n".join(formatted_rows)


def build_context(
    results: list[dict],
) -> str:
    """Build an LLM-ready context from retrieved chunks."""

    if not results:
        return ""

    context_parts = []

    for result in results:
        chunk = result["chunk"]
        text = chunk["text"]

        if chunk["section"].startswith("Table"):
            text = format_table(text)

        context_parts.append(
            f"Section: {chunk['section']}\n"
            f"Book page: {chunk['book_page_number']}\n"
            f"Similarity: {result['similarity']:.4f}\n"
            f"Content:\n{text}"
        )

    return "\n\n---\n\n".join(context_parts)
