from fastapi import APIRouter
import pandas as pd
import os


router = APIRouter(
    prefix="/cluster-summary",
    tags=["Cluster Summary"]
)


@router.get("/")
def get_cluster_summary():

    output_folder = "output"


    # Check available files
    files = os.listdir(output_folder)


    # Find cluster file automatically
    cluster_file = None


    for file in files:

        if "cluster" in file.lower():

            cluster_file = file
            break


    if cluster_file is None:

        return {
            "status": "error",
            "message": "No cluster file found",
            "available_files": files
        }


    file_path = os.path.join(
        output_folder,
        cluster_file
    )


    # Read cluster data
    df = pd.read_csv(file_path)


    # Remove unwanted index columns
    df = df.loc[
        :,
        ~df.columns.str.contains("^Unnamed")
    ]


    # Fill missing values
    df = df.fillna(0)



    # Required columns
    required_columns = [

        "company_id",
        "cluster_id",
        "cluster_name",
        "distance_from_centroid"

    ]


    # Keep only existing columns
    available_columns = [
        col
        for col in required_columns
        if col in df.columns
    ]


    df = df[available_columns]



    # Validate columns
    if "cluster_id" not in df.columns:

        return {
            "status": "error",
            "message": "Cluster columns not found",
            "available_columns": list(df.columns)
        }



    # Create cluster summary
    summary = (
        df.groupby(
            [
                "cluster_id",
                "cluster_name"
            ],
            dropna=False
        )
        .agg(

            company_count=(
                "company_id",
                "count"
            ),

            companies=(
                "company_id",
                list
            ),

            average_distance=(
                "distance_from_centroid",
                "mean"
            )

        )
        .reset_index()
    )


    return {

        "status": "success",

        "source_file": cluster_file,

        "records":
            summary.to_dict(
                orient="records"
            )

    }