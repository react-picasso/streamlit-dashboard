from google.oauth2 import service_account
from google.cloud import bigquery
from config import standings_name, project_id, dataset_id
import plotly.graph_objects as go
import streamlit as st
import pandas as pd

st.set_page_config("wide")

def background_processing():
    credentials = service_account.Credentials.from_service_account_info(
        st.secrets["gcp_service_account"]
    )

    client = bigquery.Client(credentials=credentials)

    @st.cache_data(ttl=600)
    def run_query(query):
        query_job = client.query(query)
        raw_data = query_job.result()
        data = [dict(data) for data in raw_data]
        return data
    
    query = f"""
        SELECT * FROM {project_id}.{dataset_id}.{standings_name} ORDER BY Rank
    """

    data = run_query(query)

    df = pd.DataFrame(data=data)

    df_index = pd.DataFrame(data=data)

    return df

def streamlit_app():
    df = background_processing()

    st.title("La Liga statistics for 2022/23 ⚽️")

    col1, col2 = st.columns((3,3))

    with col1:
        st.subheader("Current standings")
        st.table(df)

    with col2:
        st.subheader("Points per team")

        points = df['Points'].tolist()
        points_selection = st.slider(
            'Select a Range of Points:',
            min_value = min(points),
            max_value = max(points),
            value = (min(points), max(points))
        )

        colors = ['lightslategray',] * 20
        colors[0] = 'darkgreen'
        colors[1] = 'darkgreen'
        colors[2] = 'darkgreen'
        colors[3] = 'darkgreen'
        colors[4] = 'lightgreen'
        colors[-1] = 'crimson'
        colors[-2] = 'crimson'
        colors[-3] = 'crimson'

        mask = df['Points'].between(*points_selection)
        results = df[mask].shape[0]
        st.markdown(f"*Teams within range of selected points: {results}*")
        df_grouped = df[mask]
        df_grouped = df_grouped.reset_index()

        points_chart = go.Figure(
            data=[go.Bar(
                x = df_grouped['Team'],
                y = df_grouped['Points'],
                marker_color=colors
            )]
        )

        points_chart.update_layout(
            xaxis_tickangle=-35,
            autosize=False,
            margin=dict(
                l=0,
                r=0,
                b=0,
                t=0
            )
        )

        st.plotly_chart(points_chart, use_container_width=True)

streamlit_app()