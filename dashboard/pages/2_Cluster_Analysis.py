import streamlit as st
import requests
import pandas as pd
import plotly.express as px


API_URL = "http://127.0.0.1:8000"


st.title("📊 Cluster Analysis")


# Get cluster data

response = requests.get(
    f"{API_URL}/clusters/"
)


if response.status_code == 200:

    data = response.json()

    df = pd.DataFrame(data)


    st.subheader("Cluster Distribution")


    cluster_count = (
        df["cluster_name"]
        .value_counts()
        .reset_index()
    )

    cluster_count.columns = [
        "Cluster",
        "Companies"
    ]


    fig = px.bar(
        cluster_count,
        x="Cluster",
        y="Companies",
        title="Companies per Cluster"
    )


    st.plotly_chart(
        fig,
        use_container_width=True
    )


    st.subheader("Cluster Details")


    st.dataframe(
        df,
        use_container_width=True
    )


else:

    st.error(
        "Unable to load clusters"
    )