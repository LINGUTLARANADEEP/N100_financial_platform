import os
import pandas as pd

from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    PageBreak,
    Image
)

from reportlab.lib.styles import getSampleStyleSheet


OUTPUT_DIR = "reports/tearsheets"

os.makedirs(
    OUTPUT_DIR,
    exist_ok=True
)


RATIO_FILE = "output/financial_ratios.csv"
PROS_FILE = "output/pros_cons_generated.csv"
CAPITAL_FILE = "output/capital_allocation.csv"

CHART_DIR = "reports/radar_charts"



def load_company_data(company_id):

    ratios = pd.read_csv(RATIO_FILE)


    company = ratios[
        ratios["company_id"] == company_id
    ].copy()


    if company.empty:
        raise Exception(
            f"{company_id} not found"
        )


    latest = company.sort_values(
        "year"
    ).iloc[-1]



    pros_cons = pd.read_csv(
        PROS_FILE
    )


    pros = pros_cons[
        (pros_cons.company_id == company_id)
        &
        (pros_cons.type == "pro")
    ]["text"].tolist()



    cons = pros_cons[
        (pros_cons.company_id == company_id)
        &
        (pros_cons.type == "con")
    ]["text"].tolist()



    capital = pd.read_csv(
        CAPITAL_FILE
    )


    capital = capital[
        capital.company_id == company_id
    ].sort_values(
        "year"
    )



    pattern = "Unknown"


    if not capital.empty:

        pattern = capital.iloc[-1]["pattern_label"]



    return latest, pros, cons, pattern




def add_chart(content, path, width=300, height=180):

    if os.path.exists(path):

        content.append(
            Image(
                path,
                width=width,
                height=height
            )
        )

        content.append(
            Spacer(1,20)
        )





def generate_tearsheet(company_id):


    latest, pros, cons, pattern = load_company_data(
        company_id
    )


    file_path = (
        f"{OUTPUT_DIR}/{company_id}_tearsheet.pdf"
    )


    doc = SimpleDocTemplate(
        file_path
    )


    styles = getSampleStyleSheet()


    content = []



    # -------------------------
    # HEADER
    # -------------------------


    content.append(
        Paragraph(
            f"{company_id} Financial Tearsheet",
            styles["Title"]
        )
    )


    content.append(
        Spacer(1,20)
    )



    # -------------------------
    # KPI TABLE
    # -------------------------


    content.append(
        Paragraph(
            "Key Metrics",
            styles["Heading2"]
        )
    )



    kpis = [

    ["ROE",
     f"{latest['return_on_equity_pct']:.2f}%"],

    ["ROCE",
     latest["roce"] if "roce" in latest else "N/A"],

    ["Revenue CAGR",
     f"{latest['revenue_cagr_5yr']:.2f}%"],

    ["PAT CAGR",
     f"{latest['pat_cagr_5yr']:.2f}%"],

    ["Debt/Equity",
     f"{latest['debt_to_equity']:.2f}"],

    ["FCF",
     f"{latest['free_cash_flow_cr']:,.0f}"]

]



    table = Table(
        kpis
    )


    table.setStyle(
        TableStyle(
            [
                ("GRID",(0,0),(-1,-1),0.5,None)
            ]
        )
    )


    content.append(table)



    content.append(
        Spacer(1,20)
    )



    # -------------------------
    # CHARTS
    # -------------------------


    content.append(
        PageBreak()
    )


    content.append(
        Paragraph(
            "Financial Visual Analysis",
            styles["Heading2"]
        )
    )


    charts = [

        f"{CHART_DIR}/{company_id}_capital_structure.png",

        f"{CHART_DIR}/{company_id}_cashflow.png",

        f"{CHART_DIR}/{company_id}_cashflow_quality.png",

        f"{CHART_DIR}/{company_id}_capital_allocation.png",

        f"{CHART_DIR}/{company_id}_radar.png"

    ]



    for chart in charts:

        add_chart(
            content,
            chart
        )




    # -------------------------
    # INSIGHTS
    # -------------------------


    content.append(
        PageBreak()
    )



    content.append(
        Paragraph(
            "Strengths",
            styles["Heading2"]
        )
    )


    for p in pros[:5]:

        content.append(
            Paragraph(
                "✓ " + str(p),
                styles["Normal"]
            )
        )



    content.append(
        Spacer(1,20)
    )
        # -------------------------
    # RISKS
    # -------------------------

    content.append(
        Paragraph(
            "Risks",
            styles["Heading2"]
        )
    )


    if cons:

        for c in cons[:5]:

            content.append(
                Paragraph(
                    "✗ " + str(c),
                    styles["Normal"]
                )
            )

    else:

        content.append(
            Paragraph(
                "No significant financial risks identified based on current profitability, leverage, and cash flow indicators.",
                styles["Normal"]
            )
        )


    content.append(
        Spacer(1,20)
    )



    content.append(
        Paragraph(
            f"Capital Allocation Pattern: {pattern}",
            styles["Heading3"]
        )
    )



    doc.build(
        content
    )


    print(
        "Generated:",
        file_path
    )





if __name__ == "__main__":

    generate_tearsheet(
        "TCS"
    )