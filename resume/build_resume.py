from __future__ import annotations

import argparse
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_RIGHT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import (
    HRFlowable,
    KeepTogether,
    PageBreak,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)

from content import CONTENT


BLACK = colors.HexColor("#111111")
GRAY = colors.HexColor("#555555")
LIGHT_GRAY = colors.HexColor("#F3F3F3")


def esc(text: str) -> str:
    return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def link(url: str, label: str) -> str:
    return f'<link href="{url}" color="#111111"><u>{esc(label)}</u></link>'


def build_resume(output_path: Path, language: str = "en") -> None:
    copy = CONTENT[language]
    output_path.parent.mkdir(parents=True, exist_ok=True)
    doc = SimpleDocTemplate(
        str(output_path),
        pagesize=A4,
        leftMargin=14 * mm,
        rightMargin=14 * mm,
        topMargin=12 * mm,
        bottomMargin=11 * mm,
        title="Abderrahman Laraich - Ruby on Rails and React Engineer",
        author="Abderrahman Laraich",
        subject="Resume",
        keywords="Ruby on Rails, React, TypeScript, PostgreSQL, remote software engineer",
    )

    base = getSampleStyleSheet()
    styles = {
        "name": ParagraphStyle(
            "Name", parent=base["Normal"], fontName="Times-Bold", fontSize=25,
            leading=27, textColor=BLACK, spaceAfter=2 * mm,
        ),
        "role": ParagraphStyle(
            "Role", parent=base["Normal"], fontName="Times-Italic", fontSize=11,
            leading=13, textColor=GRAY,
        ),
        "contact": ParagraphStyle(
            "Contact", parent=base["Normal"], fontName="Times-Roman", fontSize=8.7,
            leading=11.5, textColor=BLACK, alignment=TA_RIGHT,
        ),
        "summary": ParagraphStyle(
            "Summary", parent=base["BodyText"], fontName="Times-Roman", fontSize=9.2,
            leading=12.2, textColor=BLACK,
        ),
        "section": ParagraphStyle(
            "Section", parent=base["Heading2"], fontName="Times-Bold", fontSize=11.5,
            leading=13, textColor=BLACK, spaceBefore=2.2 * mm, spaceAfter=0.8 * mm,
        ),
        "subsection": ParagraphStyle(
            "Subsection", parent=base["Normal"], fontName="Times-BoldItalic", fontSize=9.5,
            leading=11.5, textColor=GRAY, spaceBefore=1.3 * mm, spaceAfter=1.0 * mm,
        ),
        "body": ParagraphStyle(
            "Body", parent=base["BodyText"], fontName="Times-Roman", fontSize=8.8,
            leading=11.2, textColor=BLACK, spaceAfter=0.9 * mm,
        ),
        "small": ParagraphStyle(
            "Small", parent=base["BodyText"], fontName="Times-Roman", fontSize=8.2,
            leading=10.2, textColor=GRAY, spaceAfter=0.8 * mm,
        ),
        "label": ParagraphStyle(
            "Label", parent=base["BodyText"], fontName="Times-Bold", fontSize=8.8,
            leading=10.8, textColor=BLACK,
        ),
        "job": ParagraphStyle(
            "Job", parent=base["BodyText"], fontName="Times-Bold", fontSize=9.7,
            leading=11.5, textColor=BLACK,
        ),
        "jobrole": ParagraphStyle(
            "JobRole", parent=base["BodyText"], fontName="Times-Italic", fontSize=8.8,
            leading=10.8, textColor=GRAY,
        ),
        "meta": ParagraphStyle(
            "Meta", parent=base["BodyText"], fontName="Times-Roman", fontSize=8.2,
            leading=10.5, textColor=GRAY, alignment=TA_RIGHT,
        ),
        "bullet": ParagraphStyle(
            "Bullet", parent=base["BodyText"], fontName="Times-Roman", fontSize=8.7,
            leading=11.0, textColor=BLACK, leftIndent=4.3 * mm,
            firstLineIndent=-2.8 * mm, bulletIndent=0, spaceAfter=0.65 * mm,
        ),
        "project": ParagraphStyle(
            "Project", parent=base["BodyText"], fontName="Times-Bold", fontSize=9.3,
            leading=11.2, textColor=BLACK,
        ),
    }

    story = []

    header = Table(
        [[
            [Paragraph("ABDERRAHMAN LARAICH", styles["name"]),
             Paragraph(esc(copy["role"]), styles["role"])],
            Paragraph(
                f'{link("https://github.com/abdokin", "github.com/abdokin")}<br/>'
                f'{link("mailto:laarichabdo@gmail.com", "laarichabdo@gmail.com")}<br/>'
                "+212 614 292 371<br/>Casablanca, Morocco (UTC+1)<br/>" + esc(copy["remote"]),
                styles["contact"],
            ),
        ]],
        colWidths=[doc.width * 0.67, doc.width * 0.33],
        style=TableStyle([
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("LEFTPADDING", (0, 0), (-1, -1), 0),
            ("RIGHTPADDING", (0, 0), (-1, -1), 0),
            ("TOPPADDING", (0, 0), (-1, -1), 0),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
        ]),
    )
    story += [header, Spacer(1, 2.5 * mm), HRFlowable(width="100%", thickness=1.4, color=BLACK), Spacer(1, 2.2 * mm)]

    summary = Table(
        [[Paragraph(
            esc(copy["summary"]),
            styles["summary"],
        )]],
        colWidths=[doc.width],
        style=TableStyle([
            ("BACKGROUND", (0, 0), (-1, -1), LIGHT_GRAY),
            ("LINEBEFORE", (0, 0), (0, -1), 2.3, BLACK),
            ("LEFTPADDING", (0, 0), (-1, -1), 5),
            ("RIGHTPADDING", (0, 0), (-1, -1), 5),
            ("TOPPADDING", (0, 0), (-1, -1), 6),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ]),
    )
    story.append(summary)

    def section(title: str) -> None:
        story.append(Paragraph(title.upper(), styles["section"]))
        story.append(HRFlowable(width="100%", thickness=0.8, color=BLACK, spaceAfter=1.2 * mm))

    def subsection(title: str) -> None:
        story.append(Paragraph(title, styles["subsection"]))

    def bullets(items: list[str]) -> None:
        for item in items:
            story.append(Paragraph(esc(item), styles["bullet"], bulletText="-"))

    def project_header(name: str, stack: str) -> None:
        story.append(Table(
            [[Paragraph(esc(name), styles["project"]), Paragraph(esc(stack), styles["meta"])]],
            colWidths=[doc.width * 0.70, doc.width * 0.30],
            style=TableStyle([
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 0),
                ("RIGHTPADDING", (0, 0), (-1, -1), 0),
                ("TOPPADDING", (0, 0), (-1, -1), 0),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 1.0 * mm),
            ]),
        ))

    section(copy["sections"]["skills"])
    skills = copy["skills"]
    skill_table = Table(
        [[Paragraph(f"{esc(k)}:", styles["label"]), Paragraph(esc(v), styles["body"])] for k, v in skills],
        colWidths=[36 * mm, doc.width - 36 * mm],
        style=TableStyle([
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("LEFTPADDING", (0, 0), (-1, -1), 0),
            ("RIGHTPADDING", (0, 0), (-1, -1), 0),
            ("TOPPADDING", (0, 0), (-1, -1), 0),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 0.3 * mm),
        ]),
    )
    story.append(skill_table)

    section(copy["sections"]["experience"])
    story.append(Table(
        [[
            [Paragraph("Mibtech", styles["job"]), Paragraph(esc(copy["job"]["role"]), styles["jobrole"])],
            Paragraph(copy["job"]["location_date"], styles["meta"]),
        ]],
        colWidths=[doc.width * 0.72, doc.width * 0.28],
        style=TableStyle([
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("LEFTPADDING", (0, 0), (-1, -1), 0),
            ("RIGHTPADDING", (0, 0), (-1, -1), 0),
            ("TOPPADDING", (0, 0), (-1, -1), 0),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 1.0 * mm),
        ]),
    ))
    story.append(Paragraph(esc(copy["job"]["stack"]), styles["small"]))
    bullets(copy["job"]["bullets"])

    section(copy["sections"]["technical_projects"])
    subsection(copy["subsections"]["healthcare"])
    project_header(copy["projects"]["almaktabah"]["name"], "Rails, PostgreSQL, Tailwind")
    bullets(copy["projects"]["almaktabah"]["bullets"])
    story.append(Paragraph(
        f'{link("https://github.com/tasfya/almaktabah", "github.com/tasfya/almaktabah")}  |  '
        f'{link("https://3ilm.org", "3ilm.org")}', styles["small"],
    ))

    project_header(copy["projects"]["hospital"]["name"], "React, Symfony/PHP, PostgreSQL, Redis")
    bullets(copy["projects"]["hospital"]["bullets"])

    story.append(PageBreak())
    subsection(copy["subsections"]["saas"])
    project_header(copy["projects"]["testskills"]["name"], "Rails, React, PostgreSQL")
    bullets(copy["projects"]["testskills"]["bullets"])
    story.append(Paragraph(link("https://testskills.app", "testskills.app"), styles["small"]))

    section(copy["sections"]["personal_projects"])
    project_header(copy["projects"]["password"]["name"], "Rails 8, React, TypeScript, PostgreSQL")
    bullets(copy["projects"]["password"]["bullets"])
    story.append(Paragraph(link("https://github.com/abdokin/password-manager", "github.com/abdokin/password-manager"), styles["small"]))

    project_header(copy["projects"]["automata"]["name"], "Java, Maven, Graphviz")
    bullets(copy["projects"]["automata"]["bullets"])
    story.append(Paragraph(link("https://github.com/abdokin/automate-visualization", "github.com/abdokin/automate-visualization"), styles["small"]))

    project_header(copy["projects"]["minesweeper"]["name"], "C, Raylib")
    bullets(copy["projects"]["minesweeper"]["bullets"])
    story.append(Paragraph(link("https://github.com/abdokin/minesweeper", "github.com/abdokin/minesweeper"), styles["small"]))

    section(copy["sections"]["education"])
    story.append(Table(
        [[
            [Paragraph("University Hassan II Casablanca", styles["job"]),
             Paragraph(esc(copy["education"]["degree"]), styles["jobrole"])],
            Paragraph(copy["education"]["location_date"], styles["meta"]),
        ]],
        colWidths=[doc.width * 0.72, doc.width * 0.28],
        style=TableStyle([
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("LEFTPADDING", (0, 0), (-1, -1), 0),
            ("RIGHTPADDING", (0, 0), (-1, -1), 0),
            ("TOPPADDING", (0, 0), (-1, -1), 0),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 1.0 * mm),
        ]),
    ))
    story.append(Paragraph(
        esc(copy["education"]["core"]),
        styles["small"],
    ))

    section(copy["sections"]["additional"])
    additional = Table(
        [[
            Paragraph(copy["additional"]["languages"], styles["body"]),
            Paragraph(copy["additional"]["interests"], styles["body"]),
        ]],
        colWidths=[doc.width * 0.48, doc.width * 0.52],
        style=TableStyle([
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("LEFTPADDING", (0, 0), (-1, -1), 0),
            ("RIGHTPADDING", (0, 0), (-1, -1), 5 * mm),
            ("TOPPADDING", (0, 0), (-1, -1), 0),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
        ]),
    )
    story.append(KeepTogether(additional))

    doc.build(story)


def main() -> None:
    parser = argparse.ArgumentParser(description="Build Abderrahman Laraich's resume.")
    parser.add_argument("--output", type=Path, default=Path("Abderrahman-Laraich-Resume.pdf"))
    parser.add_argument("--language", choices=("en", "fr"), default="en")
    args = parser.parse_args()
    build_resume(args.output.resolve(), language=args.language)


if __name__ == "__main__":
    main()
