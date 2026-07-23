from fastapi import APIRouter
import pandas as pd
import os

router = APIRouter(
    prefix="/cluster-summary",
    tags=["Cluster Summary"]
)

@router.get("/")
def get_cluster_summary():

    file_path = "output/cluster_statistics.csv"

    df = pd.read_csv(file_path)

    # remove unwanted index column
    df = df.loc[:, ~df.columns.str.contains('^Unnamed')]

    # replace NaN values
    df = df.fillna(0)

    return {
        "status": "success",
        "records": df.to_dict(orient="records")
    }