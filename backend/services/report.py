from io import BytesIO
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
)


def build_report(
    record,
    breakdown,
    recommendations,
    prediction,
    forecast,
    fusion=None,
):
    buf = BytesIO()

    doc = SimpleDocTemplate(
        buf,
        pagesize=A4,
        rightMargin=16 * mm,
        leftMargin=16 * mm,
        topMargin=16 * mm,
        bottomMargin=16 * mm,
        title="GreenPulse AI Report",
    )

    styles = getSampleStyleSheet()
    story = []

    # Report heading and user information
    story.extend(
        [
            Paragraph("GreenPulse AI", styles["Title"]),
            Paragraph(
                "AI-Powered Carbon Footprint Report",
                styles["Heading2"],
            ),
            Paragraph(
                f"User: {record.user_name}",
                styles["BodyText"],
            ),
            Spacer(1, 10),
        ]
    )

    # Summary table
    rows = [
        ["Metric", "Result"],
        [
            "Monthly footprint",
            f"{record.monthly_emissions:.2f} kg CO2e",
        ],
        [
            "Annual footprint",
            f"{record.annual_emissions:.2f} kg CO2e",
        ],
        [
            "Sustainability score",
            f"{record.sustainability_score:.1f}/100",
        ],
        ["AI lifestyle group", record.cluster],
        [
            "AI annual prediction",
            f"{prediction:.2f} kg CO2e",
        ],
    ]

    summary_table = Table(rows, colWidths=[75 * mm, 85 * mm])
    summary_table.setStyle(
        TableStyle(
            [
                (
                    "BACKGROUND",
                    (0, 0),
                    (-1, 0),
                    colors.HexColor("#173f31"),
                ),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                (
                    "GRID",
                    (0, 0),
                    (-1, -1),
                    0.4,
                    colors.HexColor("#dce8df"),
                ),
                ("PADDING", (0, 0), (-1, -1), 6),
            ]
        )
    )

    story.extend(
        [
            Paragraph("Summary", styles["Heading2"]),
            summary_table,
        ]
    )

    # Adaptive fusion transparency table
    if fusion:
        fw = [
            ["Fusion transparency", "Value"],
            [
                "Deterministic estimate",
                f"{fusion['deterministic_estimate']:.2f} kg CO2e/year",
            ],
            [
                "Random Forest estimate",
                f"{fusion['ml_estimate']:.2f} kg CO2e/year",
            ],
            [
                "Fused estimate",
                f"{fusion['fused_estimate']:.2f} kg CO2e/year",
            ],
            [
                "AI confidence weight",
                f"{fusion['confidence_weight'] * 100:.1f}%",
            ],
            [
                "Distribution distance (S1)",
                f"{fusion['s1_distance']:.3f}",
            ],
            [
                "Cluster density (S2)",
                f"{fusion['s2_density']:.3f}",
            ],
            [
                "Historical residual (S3)",
                f"{fusion['s3_residual']:.3f}",
            ],
            [
                "Divergence detected",
                "Yes" if fusion["divergence_flag"] else "No",
            ],
        ]

        fusion_table = Table(
            fw,
            colWidths=[75 * mm, 85 * mm],
        )
        fusion_table.setStyle(
            TableStyle(
                [
                    (
                        "BACKGROUND",
                        (0, 0),
                        (-1, 0),
                        colors.HexColor("#173f31"),
                    ),
                    ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                    (
                        "GRID",
                        (0, 0),
                        (-1, -1),
                        0.4,
                        colors.HexColor("#dce8df"),
                    ),
                    ("PADDING", (0, 0), (-1, -1), 5),
                ]
            )
        )

        story.extend(
            [
                Spacer(1, 10),
                Paragraph(
                    "Adaptive Fusion Transparency",
                    styles["Heading2"],
                ),
                fusion_table,
            ]
        )

    # Emission breakdown table
    breakdown_rows = [["Source", "kg CO2e/month"]]

    for key, value in breakdown.items():
        if key != "Total":
            breakdown_rows.append([key, f"{value:.2f}"])

    breakdown_rows.append(
        ["TOTAL", f"{breakdown['Total']:.2f}"]
    )

    breakdown_table = Table(
        breakdown_rows,
        colWidths=[75 * mm, 85 * mm],
    )
    breakdown_table.setStyle(
        TableStyle(
            [
                (
                    "BACKGROUND",
                    (0, 0),
                    (-1, 0),
                    colors.HexColor("#34745c"),
                ),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                (
                    "GRID",
                    (0, 0),
                    (-1, -1),
                    0.4,
                    colors.HexColor("#dce8df"),
                ),
                ("PADDING", (0, 0), (-1, -1), 5),
            ]
        )
    )

    story.extend(
        [
            Spacer(1, 10),
            Paragraph(
                "Emission Breakdown",
                styles["Heading2"],
            ),
            breakdown_table,
            Spacer(1, 10),
            Paragraph(
                "Personalized Recommendations",
                styles["Heading2"],
            ),
        ]
    )

    # Personalized recommendations
    for recommendation in recommendations:
        story.append(
            Paragraph(
                "&#8226; " + str(recommendation),
                styles["BodyText"],
            )
        )
        story.append(Spacer(1, 4))

    # AI forecast table
    forecast_rows = [
        ["Forecast month", "Estimated kg CO2e"]
    ]

    for item in forecast:
        forecast_rows.append(
            [
                str(item["month"]),
                f"{item['estimated_emissions']:.2f}",
            ]
        )

    forecast_table = Table(
        forecast_rows,
        colWidths=[75 * mm, 85 * mm],
    )
    forecast_table.setStyle(
        TableStyle(
            [
                (
                    "BACKGROUND",
                    (0, 0),
                    (-1, 0),
                    colors.HexColor("#34745c"),
                ),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                (
                    "GRID",
                    (0, 0),
                    (-1, -1),
                    0.4,
                    colors.HexColor("#dce8df"),
                ),
                ("PADDING", (0, 0), (-1, -1), 5),
            ]
        )
    )

    story.extend(
        [
            Spacer(1, 10),
            Paragraph("AI Forecast", styles["Heading2"]),
            forecast_table,
            Spacer(1, 12),
            Paragraph(
                "Educational MVP: replace demo emission factors "
                "with documented country-specific factors for "
                "final research use.",
                styles["BodyText"],
            ),
        ]
    )

    # Generate the PDF in memory
    doc.build(story)
    buf.seek(0)

    return buf
