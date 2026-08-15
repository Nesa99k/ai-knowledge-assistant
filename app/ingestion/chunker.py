import re

from transformers import AutoTokenizer

from app.ingestion.models import Chunk
from app.ingestion.pdf_models import (
    DocumentElement,
    DocumentPage,
)


TOKENIZER_NAME = "BAAI/bge-small-en-v1.5"

BOX_TITLE_PATTERN = re.compile(
    r"^What\s+to\s+expect\s+in\s+the\s+Diet\s+Prescription$",
    re.IGNORECASE,
)

TABLE_TITLE_PATTERN = re.compile(
    r"^Table\s+1\.\s*Frequently\s+occurring\s+disabilities"
    r"(?:,\s*continued)?$",
    re.IGNORECASE,
)

TABLE_SECTION = "Table 1 - Frequently occurring disabilities"

SECTION_NAMES = [
    "Autism",
    "Cerebral Palsy",
    "Epilepsy or Seizure Disorder",
    "Muscular Dystrophy",
    "Mental Retardation",
    "Down Syndrome",
    "Prader Willi (PW) Syndrome",
    "Spina Bifida",
    "Cystic Fibrosis",
    "Rett Syndrome",
    "Metabolic Diseases",
    "Diabetes",
    "Inborn Errors of Metabolism (IEM)",
    "One Diet Does Not Fit All",
    "Diets May Need Adjustments",
    "Need for Consultants",
    "How To Handle Mistakes",
]

INITIAL_SECTION = "Chapter Introduction"

tokenizer = AutoTokenizer.from_pretrained(
    TOKENIZER_NAME
)


def normalize_text(text: str) -> str:
    return re.sub(
        r"\s+",
        " ",
        text.strip(),
    )


def normalize_section_name(
    text: str,
) -> str | None:

    normalized = normalize_text(text)

    for section in SECTION_NAMES:
        if normalized.casefold() == section.casefold():
            return section

    return None


def is_section_heading(
    element: DocumentElement,
) -> bool:

    return (
        normalize_section_name(element.text)
        is not None
    )


def get_section_name(
    element: DocumentElement,
) -> str | None:

    return normalize_section_name(
        element.text
    )


def is_box_title(
    element: DocumentElement,
) -> bool:

    return bool(
        BOX_TITLE_PATTERN.fullmatch(
            normalize_text(element.text)
        )
    )


def is_table_title(
    element: DocumentElement,
) -> bool:

    return bool(
        TABLE_TITLE_PATTERN.fullmatch(
            normalize_text(element.text)
        )
    )


def count_tokens(text: str) -> int:

    return len(
        tokenizer.encode(
            text,
            add_special_tokens=False,
        )
    )


def split_by_tokens(
    text: str,
    max_tokens: int,
) -> list[str]:

    token_ids = tokenizer.encode(
        text,
        add_special_tokens=False,
    )

    chunks = []

    for start in range(
        0,
        len(token_ids),
        max_tokens,
    ):
        token_chunk = token_ids[
            start:start + max_tokens
        ]

        chunks.append(
            tokenizer.decode(
                token_chunk,
                skip_special_tokens=True,
            )
        )

    return chunks


def split_into_sentences(
    text: str,
) -> list[str]:

    sentences = re.split(
        r"(?<=[.!?])\s+",
        text.strip(),
    )

    return [
        sentence.strip()
        for sentence in sentences
        if sentence.strip()
    ]


def assign_sections(
    elements: list[DocumentElement],
    current_section: str = INITIAL_SECTION,
) -> list[tuple[str, DocumentElement]]:

    assigned = []

    for element in elements:

        section_name = get_section_name(
            element
        )

        if section_name is not None:
            current_section = section_name

        elif (
            element.element_type == "table"
            or is_table_title(element)
        ):
            current_section = TABLE_SECTION

        assigned.append(
            (
                current_section,
                element,
            )
        )

    return assigned


def clean_table_text(
    text: str,
) -> str:
    """Remove meaningless markdown separator lines from tables."""

    lines = [
        line.strip()
        for line in text.splitlines()
        if line.strip()
    ]

    cleaned_lines = []

    for line in lines:

        stripped = line.replace("|", "").replace(
            ":", "").replace("-", "").strip()

        if not stripped:
            continue

        cleaned_lines.append(line)

    return "\n".join(cleaned_lines).strip()


def extract_semantic_blocks(
    elements: list[DocumentElement],
) -> list[tuple[str, bool, bool]]:

    blocks = []

    current_box = []
    inside_box = False

    current_table = []
    inside_table = False

    for element in elements:

        text = element.text.strip()

        if not text:
            continue

        is_table = (
            element.element_type == "table"
        )

        if is_table:

            if current_box:
                blocks.append(
                    (
                        "\n".join(current_box),
                        True,
                        False,
                    )
                )

                current_box = []
                inside_box = False

            current_table.append(text)
            inside_table = True
            continue

        if inside_table:

            table_text = clean_table_text(
                "\n".join(current_table)
            )

            if table_text:
                blocks.append(
                    (
                        table_text,
                        False,
                        True,
                    )
                )

            current_table = []
            inside_table = False

        if is_box_title(element):

            if current_box:
                blocks.append(
                    (
                        "\n".join(current_box),
                        True,
                        False,
                    )
                )

                current_box = []

            current_box.append(text)
            inside_box = True
            continue

        if inside_box:

            if is_section_heading(element):

                blocks.append(
                    (
                        "\n".join(current_box),
                        True,
                        False,
                    )
                )

                current_box = []
                inside_box = False

                blocks.append(
                    (
                        text,
                        False,
                        False,
                    )
                )

                continue

            current_box.append(text)
            continue

        if is_table_title(element):
            current_table.append(text)
            inside_table = True
        else:
            blocks.append(
                (
                    text,
                    False,
                    False,
                )
            )

    if current_table:

        table_text = clean_table_text(
            "\n".join(current_table)
        )

        if table_text:
            blocks.append(
                (
                    table_text,
                    False,
                    True,
                )
            )

    if current_box:

        blocks.append(
            (
                "\n".join(current_box),
                True,
                False,
            )
        )

    return blocks


def chunk_long_paragraph(
    paragraph: str,
    max_tokens: int,
    overlap: int,
) -> list[str]:

    sentences = split_into_sentences(
        paragraph
    )

    chunks = []
    current_sentences = []
    current_tokens = 0

    for sentence in sentences:

        sentence_tokens = count_tokens(
            sentence
        )

        if sentence_tokens > max_tokens:

            if current_sentences:

                chunks.append(
                    " ".join(
                        current_sentences
                    )
                )

                current_sentences = []
                current_tokens = 0

            chunks.extend(
                split_by_tokens(
                    sentence,
                    max_tokens,
                )
            )

            continue

        if (
            current_sentences
            and current_tokens + sentence_tokens
            > max_tokens
        ):

            chunks.append(
                " ".join(
                    current_sentences
                )
            )

            overlap_sentences = []
            overlap_tokens = 0

            for previous_sentence in reversed(
                current_sentences
            ):

                previous_tokens = count_tokens(
                    previous_sentence
                )

                if (
                    overlap_tokens
                    + previous_tokens
                    > overlap
                ):
                    break

                overlap_sentences.insert(
                    0,
                    previous_sentence,
                )

                overlap_tokens += previous_tokens

            current_sentences = []
            current_tokens = 0

            for overlap_sentence in (
                overlap_sentences
            ):

                overlap_sentence_tokens = (
                    count_tokens(
                        overlap_sentence
                    )
                )

                if (
                    current_tokens
                    + overlap_sentence_tokens
                    + sentence_tokens
                    <= max_tokens
                ):

                    current_sentences.append(
                        overlap_sentence
                    )

                    current_tokens += (
                        overlap_sentence_tokens
                    )

        current_sentences.append(
            sentence
        )

        current_tokens += sentence_tokens

    if current_sentences:

        chunks.append(
            " ".join(
                current_sentences
            )
        )

    return chunks


def create_chunk(
    text: str,
    source: str,
    section: str,
    chunk_id: int,
    page: DocumentPage,
) -> Chunk:

    return Chunk(
        text=text,
        source=source,
        section=section,
        chunk_id=chunk_id,
        pdf_page_number=page.pdf_page_number,
        book_page_number=page.book_page_number,
    )


def chunk_section(
    elements: list[DocumentElement],
    page: DocumentPage,
    source: str,
    section: str,
    chunk_size: int,
    overlap: int,
    start_chunk_id: int,
) -> list[Chunk]:

    semantic_blocks = extract_semantic_blocks(
        elements
    )

    chunks = []
    chunk_id = start_chunk_id

    current_blocks = []
    current_tokens = 0

    for block, is_box, is_table in semantic_blocks:

        block = block.strip()

        if not block:
            continue

        block_tokens = count_tokens(
            block
        )

        # --------------------------------------------------
        # TABLE
        # --------------------------------------------------

        if is_table:

            if current_blocks:

                chunks.append(
                    create_chunk(
                        text="\n\n".join(
                            current_blocks
                        ),
                        source=source,
                        section=section,
                        chunk_id=chunk_id,
                        page=page,
                    )
                )

                chunk_id += 1
                current_blocks = []
                current_tokens = 0

            chunks.append(
                create_chunk(
                    text=block,
                    source=source,
                    section=TABLE_SECTION,
                    chunk_id=chunk_id,
                    page=page,
                )
            )

            chunk_id += 1
            continue

        # --------------------------------------------------
        # BOX
        # --------------------------------------------------

        if is_box:

            if current_blocks:

                chunks.append(
                    create_chunk(
                        text="\n\n".join(
                            current_blocks
                        ),
                        source=source,
                        section=section,
                        chunk_id=chunk_id,
                        page=page,
                    )
                )

                chunk_id += 1
                current_blocks = []
                current_tokens = 0

            if block_tokens <= chunk_size:

                chunks.append(
                    create_chunk(
                        text=block,
                        source=source,
                        section=section,
                        chunk_id=chunk_id,
                        page=page,
                    )
                )

                chunk_id += 1
                continue

            long_chunks = chunk_long_paragraph(
                block,
                chunk_size,
                overlap,
            )

            for long_chunk in long_chunks:

                chunks.append(
                    create_chunk(
                        text=long_chunk,
                        source=source,
                        section=section,
                        chunk_id=chunk_id,
                        page=page,
                    )
                )

                chunk_id += 1

            continue

        # --------------------------------------------------
        # NORMAL TEXT
        # --------------------------------------------------

        if block_tokens > chunk_size:

            if current_blocks:

                chunks.append(
                    create_chunk(
                        text="\n\n".join(
                            current_blocks
                        ),
                        source=source,
                        section=section,
                        chunk_id=chunk_id,
                        page=page,
                    )
                )

                chunk_id += 1
                current_blocks = []
                current_tokens = 0

            long_chunks = chunk_long_paragraph(
                block,
                chunk_size,
                overlap,
            )

            for long_chunk in long_chunks:

                chunks.append(
                    create_chunk(
                        text=long_chunk,
                        source=source,
                        section=section,
                        chunk_id=chunk_id,
                        page=page,
                    )
                )

                chunk_id += 1

            continue

        if (
            current_blocks
            and current_tokens + block_tokens
            > chunk_size
        ):

            chunks.append(
                create_chunk(
                    text="\n\n".join(
                        current_blocks
                    ),
                    source=source,
                    section=section,
                    chunk_id=chunk_id,
                    page=page,
                )
            )

            chunk_id += 1
            current_blocks = []
            current_tokens = 0

        current_blocks.append(block)
        current_tokens += block_tokens

    if current_blocks:

        chunks.append(
            create_chunk(
                text="\n\n".join(
                    current_blocks
                ),
                source=source,
                section=section,
                chunk_id=chunk_id,
                page=page,
            )
        )

    return chunks


def chunk_pdf_page(
    page: DocumentPage,
    source: str,
    section: str = INITIAL_SECTION,
    chunk_size: int = 300,
    overlap: int = 40,
    start_chunk_id: int = 0,
) -> tuple[list[Chunk], str, int]:
    """Create section-aware chunks with continuous chunk IDs."""

    if overlap >= chunk_size:
        raise ValueError(
            "overlap must be smaller than chunk_size"
        )

    assigned_elements = assign_sections(
        page.elements,
        current_section=section,
    )

    sections: list[
        tuple[
            str,
            list[DocumentElement],
        ]
    ] = []

    for section_name, element in assigned_elements:

        if (
            not sections
            or sections[-1][0] != section_name
        ):

            sections.append(
                (
                    section_name,
                    [],
                )
            )

        sections[-1][1].append(
            element
        )

    chunks = []
    next_chunk_id = start_chunk_id

    for section_name, elements in sections:

        section_chunks = chunk_section(
            elements=elements,
            page=page,
            source=source,
            section=section_name,
            chunk_size=chunk_size,
            overlap=overlap,
            start_chunk_id=next_chunk_id,
        )

        chunks.extend(
            section_chunks
        )

        next_chunk_id += len(
            section_chunks
        )

    final_section = (
        assigned_elements[-1][0]
        if assigned_elements
        else section
    )

    return (
        chunks,
        final_section,
        next_chunk_id,
    )
