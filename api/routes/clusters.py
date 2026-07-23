from fastapi import APIRouter
import pandas as pd


router = APIRouter(
    prefix="/clusters",
    tags=["Clusters"]
)


@router.get("/")
def get_clusters():

    df = pd.read_csv(
        "output/cluster_labels.csv"
    )


    return df.to_dict(
        orient="records"
    )