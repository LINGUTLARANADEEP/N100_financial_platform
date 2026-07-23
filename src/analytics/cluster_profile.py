import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

from src.dashboard.utils.db import run_query


OUTPUT = "output"
REPORTS = "reports"


def load_data():

    query = """

    SELECT

    c.id AS company_id,
    c.company_name,
    s.broad_sector,

    fr.return_on_equity_pct,
    fr.debt_to_equity,
    fr.revenue_cagr_5yr,
    fr.free_cash_flow_cr,
    fr.operating_profit_margin_pct

    FROM companies c

    JOIN financial_ratios fr
    ON c.id = fr.company_id

    JOIN sectors s
    ON c.id = s.company_id

    WHERE fr.year='Mar 2024'

    """

    return run_query(query)



def add_clusters(df):

    clusters = pd.read_csv(
        "output/cluster_labels.csv"
    )


    df = df.merge(
        clusters[
            [
            "company_id",
            "cluster_id",
            "cluster_name"
            ]
        ],
        on="company_id",
        how="inner"
    )

    return df



def cluster_statistics(df):

    features = [

        "return_on_equity_pct",
        "debt_to_equity",
        "revenue_cagr_5yr",
        "free_cash_flow_cr",
        "operating_profit_margin_pct"

    ]


    result = (
        df.groupby("cluster_id")[features]
        .agg(
            [
            "mean",
            "median"
            ]
        )
    )


    os.makedirs(
        OUTPUT,
        exist_ok=True
    )


    result.to_csv(
        "output/cluster_statistics.csv"
    )


    print(
        "cluster_statistics.csv created"
    )



def correlation_heatmap(df):

    features=[

        "return_on_equity_pct",
        "debt_to_equity",
        "revenue_cagr_5yr",
        "free_cash_flow_cr",
        "operating_profit_margin_pct"

    ]


    corr=df[features].corr()


    os.makedirs(
        REPORTS,
        exist_ok=True
    )


    plt.figure(figsize=(8,6))


    sns.heatmap(
        corr,
        annot=True
    )


    plt.title(
        "Financial KPI Correlation"
    )


    plt.savefig(
        "reports/correlation_heatmap.png",
        bbox_inches="tight"
    )


    plt.close()


    print(
        "correlation_heatmap.png created"
    )



def portfolio_statistics(df):

    features=[

        "return_on_equity_pct",
        "debt_to_equity",
        "revenue_cagr_5yr",
        "free_cash_flow_cr",
        "operating_profit_margin_pct"

    ]


    stats=df[features].describe(
        percentiles=[
            .10,
            .25,
            .50,
            .75,
            .90
        ]
    ).T


    stats.to_csv(
        "output/portfolio_stats.csv"
    )


    print(
        "portfolio_stats.csv created"
    )

def outlier_detection(df):

    features = [

        "return_on_equity_pct",
        "debt_to_equity",
        "revenue_cagr_5yr",
        "free_cash_flow_cr",
        "operating_profit_margin_pct"

    ]


    outliers = []


    for col in features:

        Q1 = df[col].quantile(0.25)

        Q3 = df[col].quantile(0.75)

        IQR = Q3 - Q1


        lower = Q1 - 1.5 * IQR

        upper = Q3 + 1.5 * IQR


        temp = df[
            (df[col] < lower) |
            (df[col] > upper)
        ][
            [
            "company_id",
            "company_name",
            "cluster_name",
            col
            ]
        ]


        temp["metric"] = col


        outliers.append(temp)



    result = pd.concat(
        outliers,
        ignore_index=True
    )


    result.to_csv(
        "output/outlier_report.csv",
        index=False
    )


    print(
        "outlier_report.csv created"
    )


if __name__=="__main__":


    print("Loading data...")

    df=load_data()


    print(
        "Rows:",
        len(df)
    )


    df=add_clusters(df)


    print(
        "After merge:",
        len(df)
    )


    cluster_statistics(df)

    correlation_heatmap(df)

    portfolio_statistics(df)

outlier_detection(df)


print(
    "Day 37 completed"
)