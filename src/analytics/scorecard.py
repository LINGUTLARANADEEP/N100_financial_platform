import pandas as pd


def load_reports():
    """
    Load all analytics reports
    """

    cashflow = pd.read_csv("output/cashflow_kpis.csv")
    stock = pd.read_csv("output/stock_analytics.csv")
    sector = pd.read_csv("output/sector_analytics.csv")

    return cashflow, stock, sector


def build_scorecard(cashflow, stock, sector):
    """
    Merge all reports into one scorecard
    """

    # Merge Cashflow + Stock
    report = pd.merge(
        cashflow,
        stock,
        left_on="company",
        right_on="Company",
        how="left"
    )

    # Merge Sector
    report = pd.merge(
        report,
        sector,
        left_on="company",
        right_on="Company",
        how="left"
    )

    return report


def save_scorecard(report):
    """
    Save final scorecard
    """

    report.to_csv(
        "output/company_scorecard.csv",
        index=False
    )

    print("\n==============================")
    print("Company Scorecard Saved")
    print("Location : output/company_scorecard.csv")
    print("==============================")