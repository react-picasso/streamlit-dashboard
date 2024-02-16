from google.oauth2 import service_account
from google.cloud import bigquery
from config import players_name, standings_name, project_id, dataset_id
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
    
    
    standings_query = f"""
        SELECT * FROM {project_id}.{dataset_id}.{standings_name} ORDER BY Rank
    """

    players_query = f"""
        SELECT * FROM {project_id}.{dataset_id}.{players_name} ORDER BY Goals DESC
    """

    standings_data = run_query(standings_query)
    players_data = run_query(players_query)

    standings_df = pd.DataFrame(data=standings_data)
    players_df = pd.DataFrame(data=players_data)
    
    return standings_df, players_df

def streamlit_app():
    standings_df, players_df = background_processing()

    col1, col2 = st.columns((3,3))

    col3, col4, col5, col6, col7 = st.columns((1, 1, 1, 1, 1))

    with st.container():
        # Column one
        col1.title("La Liga Statistics for 2022/23 " + "⚽️")

        col1.subheader("Current standings")
        col1.table(standings_df)

        col1.subheader("Top Scorers")
        col2.subheader("Points per team:")

        points = standings_df['Points'].tolist()
        points_selection = col2.slider(
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

        mask = standings_df['Points'].between(*points_selection)
        results = standings_df[mask].shape[0]
        col2.markdown(f"*Teams within range of selected points: {results}*")
        df_grouped = standings_df[mask]
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

        col2.plotly_chart(points_chart, use_container_width=True)

    with st.container():
        # First top scorer
        col3.markdown("**{}**".format(players_df.iloc[0][0]))
        col3.markdown("**Goals:** {}".format(players_df.iloc[0][1]))
        col3.markdown("**Team:** {}".format(players_df.iloc[0][2]))
        col3.markdown("**Nationality:** {}".format(players_df.iloc[0][3]))

        # Second top scorer
        col4.markdown("**{}**".format(players_df.iloc[1][0]))
        col4.markdown("**Goals:** {}".format(players_df.iloc[1][1]))
        col4.markdown("**Team:** {}".format(players_df.iloc[1][2]))
        col4.markdown("**Nationality:** {}".format(players_df.iloc[1][3]))

        # Third top scorer
        col5.markdown("**{}**".format(players_df.iloc[2][0]))
        col5.markdown("**Goals:** {}".format(players_df.iloc[2][1]))
        col5.markdown("**Team:** {}".format(players_df.iloc[2][2]))
        col5.markdown("**Nationality:** {}".format(players_df.iloc[2][3]))

        # Fourth top scorer
        col6.markdown("**{}**".format(players_df.iloc[3][0]))
        col6.markdown("**Goals:** {}".format(players_df.iloc[3][1]))
        col6.markdown("**Team:** {}".format(players_df.iloc[3][2]))
        col6.markdown("**Nationality:** {}".format(players_df.iloc[3][3]))

        # Fifth top scorer
        col7.markdown("**{}**".format(players_df.iloc[4][0]))
        col7.markdown("**Goals:** {}".format(players_df.iloc[4][1]))
        col7.markdown("**Team:** {}".format(players_df.iloc[4][2]))
        col7.markdown("**Nationality:** {}".format(players_df.iloc[4][3]))

streamlit_app()