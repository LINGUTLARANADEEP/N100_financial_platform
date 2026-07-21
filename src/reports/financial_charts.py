import pandas as pd
import matplotlib.pyplot as plt
import os


OUTPUT = "reports/radar_charts"

os.makedirs(OUTPUT, exist_ok=True)


# =====================================
# Balance Sheet - Capital Structure
# =====================================

def balance_sheet_chart(company):

    df = pd.read_excel(
        "data/raw/balancesheet.xlsx",
        header=1
    )

    company_df = df[
        df["company_id"] == company
    ]

    if company_df.empty:
        print("Company not found in balance sheet")
        return


    latest = company_df.iloc[-1]


    labels = [
        "Equity",
        "Reserves",
        "Borrowings",
        "Other Liabilities"
    ]

    values = [
        latest["equity_capital"],
        latest["reserves"],
        latest["borrowings"],
        latest["other_liabilities"]
    ]


    plt.figure(figsize=(7,5))

    plt.bar(
        labels,
        values
    )


    plt.title(
        f"{company} Capital Structure"
    )

    plt.ylabel(
        "Amount"
    )

    plt.xticks(
        rotation=30
    )


    plt.tight_layout()


    plt.savefig(
        f"{OUTPUT}/{company}_capital_structure.png"
    )

    plt.close()



# =====================================
# Cash Flow Trend
# =====================================

def cashflow_chart(company):

    df = pd.read_excel(
        "data/raw/cashflow.xlsx",
        header=1
    )


    company_df = df[
        df["company_id"] == company
    ]


    if company_df.empty:
        print("Company not found in cashflow")
        return



    latest = company_df.tail(5)



    plt.figure(figsize=(8,5))


    plt.plot(
        latest["year"],
        latest["operating_activity"],
        marker="o",
        label="Operating Cash Flow"
    )


    plt.plot(
        latest["year"],
        latest["investing_activity"],
        marker="o",
        label="Investing Cash Flow"
    )


    plt.plot(
        latest["year"],
        latest["financing_activity"],
        marker="o",
        label="Financing Cash Flow"
    )


    plt.title(
        f"{company} Cash Flow Trend"
    )


    plt.xlabel(
        "Year"
    )


    plt.ylabel(
        "Cash Flow"
    )


    plt.legend()


    plt.xticks(
        rotation=45
    )


    plt.tight_layout()


    plt.savefig(
        f"{OUTPUT}/{company}_cashflow.png"
    )


    plt.close()



# =====================================
# Cash Flow Quality Chart
# =====================================

def cashflow_quality_chart(company):

    df = pd.read_excel(
        "output/cashflow_intelligence.xlsx"
    )


    company_df = df[
        df["company_id"] == company
    ]


    if company_df.empty:
        print("No cashflow intelligence data")
        return


    row = company_df.iloc[0]


    labels = [
        "FCF",
        "FCF Conversion %",
        "CFO Quality Score"
    ]


    values = [
        row["free_cash_flow"],
        row["fcf_conversion_pct"],
        row["cfo_quality_score"]
    ]


    plt.figure(figsize=(7,5))


    plt.bar(
        labels,
        values
    )


    plt.title(
        f"{company} Cash Flow Quality"
    )


    plt.xticks(
        rotation=30
    )


    plt.tight_layout()


    plt.savefig(
        f"{OUTPUT}/{company}_cashflow_quality.png"
    )


    plt.close()



# =====================================
# Capital Allocation Pattern
# =====================================

def capital_allocation_chart(company):

    df = pd.read_csv(
        "output/capital_allocation.csv"
    )


    company_df = df[
        df["company_id"] == company
    ]


    if company_df.empty:
        print("No capital allocation data")
        return


    counts = (
        company_df["pattern_label"]
        .value_counts()
    )


    plt.figure(figsize=(7,5))


    counts.plot(
        kind="bar"
    )


    plt.title(
        f"{company} Capital Allocation Pattern"
    )


    plt.ylabel(
        "Years"
    )


    plt.xticks(
        rotation=30
    )


    plt.tight_layout()


    plt.savefig(
        f"{OUTPUT}/{company}_capital_allocation.png"
    )


    plt.close()



# =====================================
# Main
# =====================================

if __name__ == "__main__":


    company = "TCS"


    balance_sheet_chart(company)

    cashflow_chart(company)

    cashflow_quality_chart(company)

    capital_allocation_chart(company)


    print(
        "Financial charts generated successfully"
    )