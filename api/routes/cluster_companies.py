from fastapi import APIRouter
import pandas as pd
import os


router = APIRouter(
    prefix="/cluster-companies",
    tags=["Cluster Companies"]
)


@router.get("/{cluster_id}")
def get_cluster_companies(cluster_id:int):

    file_path = "output/cluster_labels.csv"


    if not os.path.exists(file_path):
        return {
            "status":"error",
            "message":"cluster_labels.csv file not found"
        }


    df = pd.read_csv(file_path)


    # Remove unwanted columns
    df = df.loc[
        :,
        ~df.columns.str.contains("^Unnamed")
    ]


    # Filter cluster

    result = df[
        df["cluster_id"] == cluster_id
    ]


    if result.empty:

        return {
            "status":"error",
            "message":"Cluster ID not found"
        }


    return {

        "status":"success",

        "cluster_id":cluster_id,

        "company_count":len(result),

        "companies":
            result["company_id"]
            .tolist()

    }