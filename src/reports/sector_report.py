import os
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle
)
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4

from src.dashboard.utils.db import run_query


OUTPUT_DIR = "reports/sector"

os.makedirs(OUTPUT_DIR, exist_ok=True)


def generate_sector_report(sector):

    filename = (
        sector
        .replace(" ", "_")
        .replace("&", "and")
        + "_sector_report.pdf"
    )

    path = os.path.join(
        OUTPUT_DIR,
        filename
    )

    doc = SimpleDocTemplate(
        path,
        pagesize=A4
    )

    styles = getSampleStyleSheet()

    story = []

    story.append(
        Paragraph(
            f"{sector} Sector Report",
            styles["Title"]
        )
    )

    story.append(Spacer(1,20))


    # Companies
    companies = run_query(
        f"""
        SELECT 
            company_id,
            sub_sector,
            market_cap_category
        FROM sectors
        WHERE broad_sector='{sector}'
        """
    )


    if companies.empty:
        return


    story.append(
        Paragraph(
            f"Total Companies: {len(companies)}",
            styles["Heading2"]
        )
    )

    story.append(Spacer(1,15))


    data = [
        [
            "Company",
            "Sub Sector",
            "Market Cap"
        ]
    ]


    for _,row in companies.iterrows():

        data.append(
            [
                row["company_id"],
                row["sub_sector"],
                row["market_cap_category"]
            ]
        )


    table = Table(
        data,
        repeatRows=1
    )


    table.setStyle(
        TableStyle(
            [
                (
                    "GRID",
                    (0,0),
                    (-1,-1),
                    0.5,
                    None
                ),
                (
                    "VALIGN",
                    (0,0),
                    (-1,-1),
                    "TOP"
                )
            ]
        )
    )


    story.append(table)


    story.append(Spacer(1,20))


    # KPI Summary

    story.append(
        Paragraph(
            "Sector Financial Summary",
            styles["Heading2"]
        )
    )


    kpi = run_query(
    f"""
    SELECT
        AVG(roe_percentage) as avg_roe,
        AVG(roce_percentage) as avg_roce
    FROM companies c
    JOIN sectors s
    ON c.id=s.company_id
    WHERE s.broad_sector='{sector}'
    """
)


    if not kpi.empty:

        summary = [
            [
                "Metric",
                "Value"
            ],
            [
                "Average ROE",
                str(round(kpi.iloc[0]["avg_roe"],2))
            ],
            [
                "Average ROCE",
                str(round(kpi.iloc[0]["avg_roce"],2))
            ]
        ]


        t = Table(summary)

        t.setStyle(
            TableStyle(
                [
                    (
                    "GRID",
                    (0,0),
                    (-1,-1),
                    0.5,
                    None
                    )
                ]
            )
        )

        story.append(t)


    doc.build(story)

    print(
        "Generated:",
        path
    )



def run_all():

    sectors = run_query(
        """
        SELECT DISTINCT broad_sector
        FROM sectors
        """
    )


    for sector in sectors["broad_sector"]:

        print(
            "Generating:",
            sector
        )

        generate_sector_report(
            sector
        )



if __name__=="__main__":
    run_all()