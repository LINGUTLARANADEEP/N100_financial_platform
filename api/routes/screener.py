from fastapi import APIRouter, Query
import pandas as pd
import os


router = APIRouter(
    prefix="/screener",
    tags=["Company Screener"]
)


@router.get("/")
def company_screener(

    roe: float | None = Query(
        None,
        description="Minimum Return on Equity %",
        examples=[15]
    ),

    debt: float | None = Query(
        None,
        description="Maximum Debt to Equity",
        example=1
    ),

    margin: float | None = Query(
        None,
        description="Minimum Operating Profit Margin %",
        example=20
    ),

    revenue_growth: float | None = Query(
        None,
        description="Minimum Revenue CAGR 5 Year",
        example=10
    ),

    sort_by: str = Query(
        "composite_quality_score",
        description="Sort metric"
    ),

    descending: bool = Query(
        True,
        description="Sort descending order"
    ),

    limit: int = Query(
        20,
        description="Number of companies",
        ge=1,
        le=100
    )

):


    file_path = "output/financial_ratios.csv"


    # Check file

    if not os.path.exists(file_path):

        return {
            "status": "error",
            "message": "financial_ratios.csv not found"
        }


    # Load CSV

    try:

        df = pd.read_csv(file_path)

    except Exception as e:

        return {
            "status":"error",
            "message":str(e)
        }



    # Remove unnamed columns

    df = df.loc[
        :,
        ~df.columns.str.contains("^Unnamed")
    ]



    # Convert numeric columns

    numeric_cols = [

        "return_on_equity_pct",
        "debt_to_equity",
        "operating_profit_margin_pct",
        "revenue_cagr_5yr",
        "pat_cagr_5yr",
        "eps_cagr_5yr"

    ]


    for col in numeric_cols:

        if col in df.columns:

            df[col] = pd.to_numeric(
                df[col],
                errors="coerce"
            )



    # Fix abnormal percentage values

    percentage_cols = [

        "return_on_equity_pct",
        "operating_profit_margin_pct",
        "revenue_cagr_5yr",
        "pat_cagr_5yr",
        "eps_cagr_5yr"

    ]


    for col in percentage_cols:

        if col in df.columns:

            df[col] = df[col].apply(
                lambda x: x/10 if pd.notnull(x) and x > 200 else x
            )



    # Latest year data

    if (
        "year" in df.columns
        and
        "company_id" in df.columns
    ):


        df["year"] = pd.to_datetime(
            df["year"],
            format="mixed",
            errors="coerce"
        )


        df = (
            df
            .sort_values("year")
            .groupby("company_id")
            .tail(1)
        )



    filtered = df.copy()



    # ----------------------------------
    # Composite Quality Score
    # ----------------------------------


    score_columns = [

        "return_on_equity_pct",
        "operating_profit_margin_pct",
        "revenue_cagr_5yr",
        "pat_cagr_5yr",
        "eps_cagr_5yr"

    ]


    available_scores = [

        col for col in score_columns
        if col in filtered.columns

    ]



    if available_scores:


        normalized = filtered[
            available_scores
        ].rank(
            pct=True
        )


        quality_score = (
            normalized.mean(axis=1) * 100
        )


        # Debt penalty

        if "debt_to_equity" in filtered.columns:


            debt_penalty = (
                filtered["debt_to_equity"]
                .rank(pct=True)
                * 20
            )


            quality_score = (
                quality_score - debt_penalty
            )


        filtered["composite_quality_score"] = (
            quality_score.clip(0,100)
        )


    else:

        filtered["composite_quality_score"] = 0




    # ----------------------------------
    # Filters
    # ----------------------------------


    if roe is not None and "return_on_equity_pct" in filtered.columns:

        filtered = filtered[
            filtered["return_on_equity_pct"] >= roe
        ]



    if debt is not None and "debt_to_equity" in filtered.columns:

        filtered = filtered[
            filtered["debt_to_equity"] <= debt
        ]



    if margin is not None and "operating_profit_margin_pct" in filtered.columns:

        filtered = filtered[
            filtered["operating_profit_margin_pct"] >= margin
        ]



    if revenue_growth is not None and "revenue_cagr_5yr" in filtered.columns:

        filtered = filtered[
            filtered["revenue_cagr_5yr"] >= revenue_growth
        ]




    # Output columns

    columns = [

        "company_id",
        "return_on_equity_pct",
        "debt_to_equity",
        "operating_profit_margin_pct",
        "revenue_cagr_5yr",
        "pat_cagr_5yr",
        "eps_cagr_5yr",
        "composite_quality_score"

    ]



    available_columns = [

        c for c in columns
        if c in filtered.columns

    ]



    result_df = filtered[
        available_columns
    ].copy()



    # Empty result

    if result_df.empty:

        return {

            "status":"success",
            "count":0,
            "companies":[],
            "message":"No companies found"

        }



    # Sorting

    if sort_by in result_df.columns:


        result_df[sort_by] = pd.to_numeric(
            result_df[sort_by],
            errors="coerce"
        )


        result_df = result_df.sort_values(
            by=sort_by,
            ascending=not descending,
            na_position="last"
        )


    else:

        sort_by="company_id"


        result_df = result_df.sort_values(
            by=sort_by
        )



    # Limit

    result_df = result_df.head(limit)



    # Round values

    result_df = result_df.round(2)



    # JSON cleanup

    result_df = result_df.replace(
        [
            float("inf"),
            float("-inf")
        ],
        None
    )


    result_df = result_df.where(
        pd.notnull(result_df),
        None
    )



    companies = result_df.to_dict(
        orient="records"
    )



    return {


        "status":"success",


        "filters":{

            "roe":roe,
            "debt":debt,
            "margin":margin,
            "revenue_growth":revenue_growth

        },


        "sorting":{

            "sort_by":sort_by,
            "descending":descending

        },


        "count":len(companies),


        "companies":companies

    }