import streamlit as st
import requests
import pandas as pd


API_URL = "http://127.0.0.1:8000"


st.title("🏢 Company Explorer")


response = requests.get(
    f"{API_URL}/companies/"
)


if response.status_code == 200:

    companies = response.json()

    df = pd.DataFrame(companies)


    search = st.text_input(
        "Search Company"
    )


    if search:

        df = df[
            df["company_name"]
            .str.contains(
                search,
                case=False
            )
        ]


    st.dataframe(
        df,
        use_container_width=True
    )


else:

    st.error(
        "Unable to fetch companies"
    )