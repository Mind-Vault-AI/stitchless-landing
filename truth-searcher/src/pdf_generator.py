"""
PDF Generator Module - Phase 3: The "Who" (Customer Centric Output)
Generates clean, accessible PDF reports in Dutch.
DMAIC Principle: Control output quality for customer satisfaction.
"""

import io
import logging
from datetime import datetime
from typing import Optional

from .review_analyzer import ProductAnalysisResult

logger = logging.getLogger(__name__)


def generate_pdf_report(
    analysis_result: ProductAnalysisResult,
    simplified_summary: Optional[str] = None,
) -> bytes:
    """
    Generate a PDF report from the analysis result.

    Args:
        analysis_result: The complete product analysis
        simplified_summary: Optional simplified summary text

    Returns:
        PDF file as bytes
    """
    try:
        from reportlab.lib import colors
        from reportlab.lib.pagesizes import A4
        from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
        from reportlab.lib.units import cm
        from reportlab.platypus import (
            Paragraph,
            SimpleDocTemplate,
            Spacer,
            Table,
            TableStyle,
        )
    except ImportError:
        logger.error("reportlab not installed. Run: pip install reportlab")
        raise ImportError("reportlab package required for PDF generation")

    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=2 * cm,
        leftMargin=2 * cm,
        topMargin=2 * cm,
        bottomMargin=2 * cm,
    )

    # Styles
    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        "CustomTitle",
        parent=styles["Heading1"],
        fontSize=24,
        spaceAfter=20,
        textColor=colors.HexColor("#1a365d"),
    )

    subtitle_style = ParagraphStyle(
        "CustomSubtitle",
        parent=styles["Heading2"],
        fontSize=14,
        spaceAfter=10,
        textColor=colors.HexColor("#4a5568"),
    )

    body_style = ParagraphStyle(
        "CustomBody",
        parent=styles["Normal"],
        fontSize=11,
        spaceAfter=8,
        leading=14,
    )

    small_style = ParagraphStyle(
        "Small",
        parent=styles["Normal"],
        fontSize=9,
        textColor=colors.HexColor("#718096"),
    )

    # Build document content
    story = []

    # Title
    story.append(Paragraph("🔍 De Waarheidszoeker", title_style))
    story.append(Paragraph("Eerlijk productonderzoek zonder verzinsels", subtitle_style))
    story.append(Spacer(1, 0.5 * cm))

    # Product info
    story.append(
        Paragraph(f"<b>Product:</b> {analysis_result.product_name}", body_style)
    )
    story.append(
        Paragraph(f"<b>Categorie:</b> {analysis_result.category}", body_style)
    )
    story.append(
        Paragraph(
            f"<b>Betrouwbaarheid:</b> {_get_confidence_text(analysis_result.confidence_level)}",
            body_style,
        )
    )
    story.append(
        Paragraph(
            f"<b>Aantal reviews geanalyseerd:</b> {analysis_result.total_reviews_analyzed}",
            body_style,
        )
    )
    story.append(Spacer(1, 0.5 * cm))

    # Simplified summary if available
    if simplified_summary:
        story.append(Paragraph("<b>Samenvatting (simpel uitgelegd):</b>", subtitle_style))
        story.append(Paragraph(simplified_summary, body_style))
        story.append(Spacer(1, 0.5 * cm))

    # Scores table
    story.append(Paragraph("<b>Scores per factor:</b>", subtitle_style))

    table_data = [["Wat is belangrijk?", "Score", "Uitleg"]]

    for analysis in analysis_result.analyses:
        score_display = f"{analysis.score} {analysis.score_emoji}"
        # Truncate summary if too long
        summary = analysis.summary[:100] + "..." if len(analysis.summary) > 100 else analysis.summary

        table_data.append([analysis.factor, score_display, summary])

    table = Table(table_data, colWidths=[5 * cm, 2.5 * cm, 9 * cm])
    table.setStyle(
        TableStyle(
            [
                # Header
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#2d3748")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("FONTSIZE", (0, 0), (-1, 0), 11),
                ("BOTTOMPADDING", (0, 0), (-1, 0), 12),
                ("TOPPADDING", (0, 0), (-1, 0), 12),
                # Body
                ("BACKGROUND", (0, 1), (-1, -1), colors.HexColor("#f7fafc")),
                ("FONTNAME", (0, 1), (-1, -1), "Helvetica"),
                ("FONTSIZE", (0, 1), (-1, -1), 10),
                ("BOTTOMPADDING", (0, 1), (-1, -1), 8),
                ("TOPPADDING", (0, 1), (-1, -1), 8),
                # Grid
                ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#e2e8f0")),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                # Alternating rows
                *[
                    ("BACKGROUND", (0, i), (-1, i), colors.white)
                    for i in range(2, len(table_data), 2)
                ],
            ]
        )
    )
    story.append(table)
    story.append(Spacer(1, 0.5 * cm))

    # Unit Economics
    story.append(Paragraph("<b>Prijs-kwaliteit analyse:</b>", subtitle_style))
    story.append(
        Paragraph(
            f"<b>Verhouding:</b> {analysis_result.unit_economics.price_value_ratio}",
            body_style,
        )
    )
    story.append(
        Paragraph(
            f"<b>Advies:</b> {analysis_result.unit_economics.recommendation}",
            body_style,
        )
    )
    story.append(Spacer(1, 0.5 * cm))

    # Sources
    story.append(Paragraph("<b>Bronnen:</b>", subtitle_style))
    all_sources = set()
    for analysis in analysis_result.analyses:
        all_sources.update(analysis.sources)

    if all_sources:
        for source in list(all_sources)[:10]:  # Limit to 10 sources
            # Truncate long URLs
            display_url = source[:70] + "..." if len(source) > 70 else source
            story.append(Paragraph(f"• {display_url}", small_style))
    else:
        story.append(Paragraph("Geen specifieke bronnen beschikbaar.", small_style))

    story.append(Spacer(1, 1 * cm))

    # Legend
    story.append(Paragraph("<b>Wat betekenen de scores?</b>", subtitle_style))
    legend_data = [
        ["Score", "Betekenis"],
        ["8-10 ✅", "Uitstekend - Zeer goed beoordeeld"],
        ["5-7 ⚠️", "Redelijk - Gemiddeld beoordeeld"],
        ["1-4 ❌", "Matig - Slecht beoordeeld"],
        ["N/A 🔍", "Geen data - Niet genoeg informatie gevonden"],
    ]

    legend_table = Table(legend_data, colWidths=[3 * cm, 10 * cm])
    legend_table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#edf2f7")),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("FONTSIZE", (0, 0), (-1, -1), 9),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
                ("TOPPADDING", (0, 0), (-1, -1), 6),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#e2e8f0")),
            ]
        )
    )
    story.append(legend_table)
    story.append(Spacer(1, 1 * cm))

    # Footer
    timestamp = datetime.now().strftime("%d-%m-%Y %H:%M")
    story.append(
        Paragraph(
            f"Gegenereerd door De Waarheidszoeker op {timestamp}",
            small_style,
        )
    )
    story.append(
        Paragraph(
            "⚠️ Dit rapport is gebaseerd op publiek beschikbare informatie. "
            "Controleer altijd meerdere bronnen voordat je een aankoopbeslissing neemt.",
            small_style,
        )
    )

    # Build PDF
    doc.build(story)
    buffer.seek(0)

    return buffer.getvalue()


def _get_confidence_text(confidence: str) -> str:
    """Convert confidence level to readable text with emoji."""
    mapping = {
        "hoog": "🟢 Hoog - Veel betrouwbare bronnen",
        "gemiddeld": "🟡 Gemiddeld - Voldoende bronnen",
        "laag": "🔴 Laag - Weinig bronnen gevonden",
    }
    return mapping.get(confidence, "🔍 Onbekend")


def generate_simple_text_report(
    analysis_result: ProductAnalysisResult,
    simplified_summary: Optional[str] = None,
) -> str:
    """
    Generate a simple text report (fallback if PDF generation fails).

    Args:
        analysis_result: The complete product analysis
        simplified_summary: Optional simplified summary text

    Returns:
        Plain text report
    """
    lines = [
        "=" * 50,
        "🔍 DE WAARHEIDSZOEKER",
        "Eerlijk productonderzoek zonder verzinsels",
        "=" * 50,
        "",
        f"Product: {analysis_result.product_name}",
        f"Categorie: {analysis_result.category}",
        f"Betrouwbaarheid: {analysis_result.confidence_level}",
        f"Reviews geanalyseerd: {analysis_result.total_reviews_analyzed}",
        "",
    ]

    if simplified_summary:
        lines.extend(["SAMENVATTING:", simplified_summary, ""])

    lines.append("SCORES:")
    lines.append("-" * 40)

    for analysis in analysis_result.analyses:
        lines.append(f"{analysis.factor}: {analysis.score} {analysis.score_emoji}")
        lines.append(f"  → {analysis.summary}")
        lines.append("")

    lines.extend([
        "-" * 40,
        "PRIJS-KWALITEIT:",
        f"Verhouding: {analysis_result.unit_economics.price_value_ratio}",
        f"Advies: {analysis_result.unit_economics.recommendation}",
        "",
        "-" * 40,
        "LEGENDA:",
        "8-10 ✅ = Uitstekend",
        "5-7 ⚠️ = Redelijk",
        "1-4 ❌ = Matig",
        "N/A 🔍 = Geen data",
        "",
        "=" * 50,
    ])

    return "\n".join(lines)
