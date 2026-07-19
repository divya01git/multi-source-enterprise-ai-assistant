from pathlib import Path
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet

# Folders
SOURCE_DIR = Path("documents/source")
OUTPUT_DIR = Path("documents/generated")

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

styles = getSampleStyleSheet()
title_style = styles["Heading1"]
heading_style = styles["Heading2"]
normal_style = styles["BodyText"]

for md_file in SOURCE_DIR.glob("*.md"):
    pdf_path = OUTPUT_DIR / f"{md_file.stem}.pdf"

    doc = SimpleDocTemplate(str(pdf_path))
    story = []

    with open(md_file, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()

            if not line:
                continue

            if line.startswith("# "):
                story.append(Paragraph(line[2:], title_style))

            elif line.startswith("## "):
                story.append(Paragraph(line[3:], heading_style))

            else:
                story.append(Paragraph(line, normal_style))

    doc.build(story)

    print(f"✅ Generated: {pdf_path.name}")

print("\n🎉 All PDFs generated successfully!")