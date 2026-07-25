from fastapi import APIRouter, HTTPException
import pandas as pd


router = APIRouter()


@router.get("/cluster-profile/{cluster_id}")
def get_cluster_profile(cluster_id: int):

    try:

        df = pd.read_csv(
            "output/cluster_labels.csv"
        )

        result = df[df["cluster_id"] == cluster_id]


        if result.empty:
            raise HTTPException(
                status_code=404,
                detail="Cluster not found"
            )


        return {
            "cluster_id": cluster_id,
            "companies": result.to_dict(
                orient="records"
            )
        }


    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )