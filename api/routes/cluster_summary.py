from fastapi import APIRouter
import pandas as pd


router = APIRouter(
    prefix="/cluster-summary",
    tags=["Cluster Summary"]
)


@router.get("/")
def get_cluster_summary():

    file_path = "output/financial_ratios.csv"


    df = pd.read_csv(file_path)


    # Remove unwanted index columns

    df = df.loc[
        :,
        ~df.columns.str.contains("^Unnamed")
    ]


    # Replace missing values

    df = df.fillna(0)


    # Keep only required columns

    required_columns = [

        "company_id",
        "company_id",
        "year",
        "return_on_equity_pct",
        "debt_to_equity",
        "operating_profit_margin_pct",
        "free_cash_flow_cr",
        "revenue_cagr_5yr",
        "composite_quality_score"

    ]


    df = df[
        [
            col
            for col in required_columns
            if col in df.columns
        ]
    ]


    return {

        "status":"success",

        "records":
            df.to_dict(
                orient="records"
            )

    }