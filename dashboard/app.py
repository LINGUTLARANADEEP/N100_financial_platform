import streamlit as st
import requests
import pandas as pd


st.set_page_config(
    page_title="N100 Financial Platform",
    page_icon="📊",
    layout="wide"
)


API_URL = "http://127.0.0.1:8000"


st.title("📊 N100 Financial Platform")


st.write("""
Financial Analytics Dashboard

Modules:
- Company Explorer
- Cluster Analysis
- Financial Metrics
""")


# -------------------------
# API CONNECTION CHECK
# -------------------------

st.sidebar.header("API Status")


try:
    response = requests.get(f"{API_URL}/companies/")

    if response.status_code == 200:
        st.sidebar.success("API Connected ✅")
    else:
        st.sidebar.error("API Error")

except Exception:
    st.sidebar.error("API Not Running")


# -------------------------
# KPI SECTION
# -------------------------

st.header("Platform Overview")


col1, col2, col3 = st.columns(3)


# Companies count

try:

    companies = requests.get(
        f"{API_URL}/companies/"
    ).json()

    total_companies = len(companies)

except:
    total_companies = 0



# Cluster count

try:

    clusters = requests.get(
        f"{API_URL}/clusters/"
    ).json()

    total_clusters = len(set(
        item["cluster_id"]
        for item in clusters
    ))

except:
    total_clusters = 0



with col1:
    st.metric(
        "Total Companies",
        total_companies
    )


with col2:
    st.metric(
        "Total Clusters",
        total_clusters
    )


with col3:
    st.metric(
        "Platform",
        "N100"
    )



# -------------------------
# COMPANY TABLE
# -------------------------

st.header("Company Database")


try:

    df = pd.DataFrame(companies)

    st.dataframe(
        df,
        use_container_width=True
    )

except:

    st.warning(
        "Unable to load companies"
    )