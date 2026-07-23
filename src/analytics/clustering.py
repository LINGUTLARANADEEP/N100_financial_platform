import os
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans

from src.dashboard.utils.db import run_query


OUTPUT = "output"
REPORTS = "reports"


def load_cluster_data():

    query = """

    WITH latest_year AS (

        SELECT 
            company_id,
            MAX(
                CASE 
                    WHEN substr(year,1,3)='Mar' THEN 
                        CAST(substr(year,5,4) AS INTEGER)

                    WHEN substr(year,1,3)='Sep' THEN
                        CAST(substr(year,5,4) AS INTEGER)

                    ELSE 0

                END
            ) AS latest_year

        FROM financial_ratios

        GROUP BY company_id
    )


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


    JOIN latest_year ly

    ON fr.company_id = ly.company_id


    JOIN sectors s

    ON c.id = s.company_id


    WHERE

    (
        CASE

        WHEN substr(fr.year,1,3)='Mar'
        THEN CAST(substr(fr.year,5,4) AS INTEGER)

        WHEN substr(fr.year,1,3)='Sep'
        THEN CAST(substr(fr.year,5,4) AS INTEGER)

        ELSE 0

        END
    )

    =
    
    ly.latest_year


    """

    df = run_query(query)

    return df



def prepare_features(df):

    features = [
        "return_on_equity_pct",
        "debt_to_equity",
        "revenue_cagr_5yr",
        "free_cash_flow_cr",
        "operating_profit_margin_pct"
    ]


    # Sector median imputation

    for col in features:

     df[col] = (
        df[col]
        .fillna(df[col].median())
    )


    # If any remaining nulls
    df[features] = (
        df[features]
        .fillna(df[features].median())
    )


    X = df[features]


    scaler = StandardScaler()

    X_scaled = scaler.fit_transform(X)


    return X_scaled



def elbow_plot(X):

    inertia = []


    for k in range(2,11):

        model = KMeans(
            n_clusters=k,
            random_state=42,
            n_init=10
        )

        model.fit(X)

        inertia.append(model.inertia_)



    plt.figure(figsize=(8,5))


    plt.plot(
        range(2,11),
        inertia,
        marker="o"
    )


    plt.xlabel("Number of clusters")
    plt.ylabel("Inertia")
    plt.title("KMeans Elbow Plot")


    os.makedirs(
        REPORTS,
        exist_ok=True
    )


    plt.savefig(
        "reports/elbow_plot.png",
        bbox_inches="tight"
    )

    plt.close()



def run_clustering():

    print("Loading data...")


    df = load_cluster_data()


    print(
        "Companies loaded:",
        len(df)
    )


    X = prepare_features(df)


    print("Generating elbow plot...")

    elbow_plot(X)



    print("Running KMeans...")


    model = KMeans(
        n_clusters=5,
        random_state=42,
        n_init=10
    )


    df["cluster_id"] = model.fit_predict(X)



    distances = model.transform(X)


    df["distance_from_centroid"] = (
        distances.min(axis=1)
    )



    cluster_names = {

        0: "High Quality Compounders",

        1: "Defensive Dividend Payers",

        2: "Value Cyclicals",

        3: "Turnaround Companies",

        4: "Emerging Growth"

    }


    df["cluster_name"] = (
        df["cluster_id"]
        .map(cluster_names)
    )



    result = df[
        [
            "company_id",
            "cluster_id",
            "cluster_name",
            "distance_from_centroid"
        ]
    ]



    os.makedirs(
        OUTPUT,
        exist_ok=True
    )


    result.to_csv(
        "output/cluster_labels.csv",
        index=False
    )


    print(
        "Saved output/cluster_labels.csv"
    )



if __name__ == "__main__":

    run_clustering()