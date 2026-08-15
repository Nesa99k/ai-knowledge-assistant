from app.ingestion.loader import (
    clean_text,
    get_book_page_number,
    load_pdf,
)


def test_clean_text_removes_header_and_footer():
    """Test that repeated header and footer are removed."""

    text = """Handbook for Children with Special Food and Nutrition Needs
Some useful content.
National Food Service Management Institute
"""

    cleaned = clean_text(text)

    assert (
        "Handbook for Children with Special Food and Nutrition Needs"
        not in cleaned
    )

    assert (
        "National Food Service Management Institute"
        not in cleaned
    )

    assert "Some useful content." in cleaned


def test_get_book_page_number():
    """Test mapping from PDF page number to printed book page."""

    assert get_book_page_number(1) is None
    assert get_book_page_number(2) is None
    assert get_book_page_number(3) == 15
    assert get_book_page_number(12) == 24


def test_load_pdf_skips_empty_pages():
    """Test that empty PDF pages are excluded from the result."""

    pages = load_pdf(
        "data/documents/disabilities.pdf"
    )

    assert pages

    assert all(
        any(
            element.text.strip()
            for element in page.elements
        )
        for page in pages
    )


def test_load_pdf_preserves_page_metadata():
    """Test that PDF and book page numbers are preserved."""

    pages = load_pdf(
        "data/documents/disabilities.pdf"
    )

    page_24 = next(
        page
        for page in pages
        if page.book_page_number == 24
    )

    assert page_24.pdf_page_number == 12
    assert page_24.book_page_number == 24
