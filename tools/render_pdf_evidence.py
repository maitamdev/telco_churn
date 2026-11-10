"""Render a reviewed Office PDF using the bundled Python runtime."""
import argparse
import json
from pathlib import Path

import pypdfium2 as pdfium
from pypdf import PdfReader


def render(source, output):
    output.mkdir(parents=True, exist_ok=True)
    pdf = pdfium.PdfDocument(source)
    reader = PdfReader(source)
    pages = []
    for index in range(len(pdf)):
        page = pdf[index]
        image = page.render(scale=1.35).to_pil()
        image.save(output / f"page-{index + 1:02}.png")
        pages.append({"page": index + 1, "text": reader.pages[index].extract_text(),
                      "size": list(image.size)})
        page.close()
    pdf.close()
    (output / "pages.json").write_text(json.dumps(pages, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Rendered {len(pages)} pages: {output}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("source", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    render(args.source, args.output)
