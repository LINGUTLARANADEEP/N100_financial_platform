from fastapi import APIRouter
import pandas as pd
import os


router = APIRouter(
    prefix="/cluster-profile",
    tags=["Cluster Profile"]
)


@router.get("/{cluster_id}")
def get_cluster_profile(cluster_id: int):

    cluster_file = "output/cluster_labels.csv"
    financial_file = "output/financial_ratios.csv"


    # Check files
    if not os.path.exists(cluster_file):
        return {
            "status": "error",
            "message": "cluster_labels.csv not found"
        }


    if not os.path.exists(financial_file):
        return {
            "status": "error",
            "message": "financial_ratios.csv not found"
        }



    # Load data
    cluster_df = pd.read_csv(cluster_file)
    financial_df = pd.read_csv(financial_file)



    # Remove unnamed columns
    cluster_df = cluster_df.loc[
        :,
        ~cluster_df.columns.str.contains("^Unnamed")
    ]

    financial_df = financial_df.loc[
        :,
        ~financial_df.columns.str.contains("^Unnamed")
    ]



    # Filter cluster
    cluster_data = cluster_df[
        cluster_df["cluster_id"] == cluster_id
    ]


    if cluster_data.empty:
        return {
            "status": "error",
            "message": "Cluster not found"
        }



    # Cluster information
    cluster_name = cluster_data[
        "cluster_name"
    ].iloc[0]


    companies = cluster_data[
        "company_id"
    ].tolist()



    # Financial data for cluster companies
    profile_df = financial_df[
        financial_df["company_id"].isin(companies)
    ]



    if profile_df.empty:
        return {
            "status": "error",
            "message": "Financial data not found"
        }



    # Convert year
    profile_df = profile_df.copy()

    profile_df["year"] = pd.to_datetime(
        profile_df["year"],
        errors="coerce"
    )



    # Latest financial record per company

    latest_profile = (
        profile_df
        .sort_values("year")
        .groupby("company_id")
        .tail(1)
    )



    # Company financial profile

    columns = [

        "company_id",
        "year",
        "return_on_equity_pct",
        "debt_to_equity",
        "operating_profit_margin_pct",
        "free_cash_flow_cr",
        "revenue_cagr_5yr",
        "pat_cagr_5yr",
        "eps_cagr_5yr",
        "composite_quality_score"

    ]


    available_columns = [
        col for col in columns
        if col in latest_profile.columns
    ]


    company_profile = (
        latest_profile[available_columns]
        .fillna(0)
        .to_dict(
            orient="records"
        )
    )



    # Cluster average metrics

    metrics = {}


    numeric_columns = [

        "return_on_equity_pct",
        "debt_to_equity",
        "operating_profit_margin_pct",
        "free_cash_flow_cr",
        "revenue_cagr_5yr",
        "pat_cagr_5yr",
        "eps_cagr_5yr",
        "composite_quality_score"

    ]


    for col in numeric_columns:

        if col in latest_profile.columns:

            metrics[col] = round(
                latest_profile[col]
                .mean(),
                2
            )



    # Top companies based on ROE

    top_companies = (

        latest_profile
        .sort_values(
            by="return_on_equity_pct",
            ascending=False
        )
        .head(10)

    )


    top_available_columns = [

        col for col in [

            "company_id",
            "return_on_equity_pct",
            "operating_profit_margin_pct",
            "free_cash_flow_cr"

        ]

        if col in top_companies.columns

    ]


    top_companies = (

        top_companies[
            top_available_columns
        ]
        .fillna(0)
        .to_dict(
            orient="records"
        )

    )



    return {

        "status": "success",

        "cluster_id": cluster_id,

        "cluster_name": cluster_name,

        "company_count": len(companies),

        "cluster_average_metrics": metrics,

        "top_companies": top_companies,

        "company_profiles": company_profile,

        "companies": company_profile

    }