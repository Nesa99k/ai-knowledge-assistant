from docling.document_converter import DocumentConverter


converter = DocumentConverter()

result = converter.convert(
    "data/documents/disabilities.pdf"
)

document = result.document

print(
    f"Tables: {len(document.tables)}"
)

for index, table in enumerate(
    document.tables
):
    print("=" * 80)
    print(f"TABLE {index}")
    print(table.export_to_markdown())
