from fastapi import APIRouter
from api.database import get_connection
import pandas as pd
import numpy as np


router = APIRouter(
    prefix="/financial-metrics",
    tags=["Financial Metrics"]
)


@router.get("/")
def get_financial_metrics():

    conn = get_connection()

    query = """
        SELECT *
        FROM financial_ratios
    """

    df = pd.read_sql_query(
        query,
        conn
    )

    conn.close()


    df = df.replace(
        [np.inf, -np.inf],
        None
    )

    df = df.where(
        pd.notnull(df),
        None
    )


    return {
        "status": "success",
        "records": df.to_dict(
            orient="records"
        )
    }