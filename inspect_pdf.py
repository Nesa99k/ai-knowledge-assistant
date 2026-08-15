from app.ingestion.loader import load_pdf


pages = load_pdf(
    "data/documents/disabilities.pdf"
)

print(f"Total pages: {len(pages)}")

for page in pages:
    if page.pdf_page_number in (12, 13):
        print("=" * 80)
        print(f"PDF page: {page.pdf_page_number}")

        for index, element in enumerate(page.elements):
            print("-" * 60)
            print(
                f"[{index}] "
                f"type={element.element_type}"
            )
            print(element.text)
