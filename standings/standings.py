from config import rapid_api, table_name, dataset_id, project_id
import pandas as pd
import requests
import json
import matplotlib.pyplot as plt
from google.cloud import bigquery

from pprint import pprint

url = 'https://api-football-v1.p.rapidapi.com/v3/standings'

headers = {
    "X-RapidAPI-Key": rapid_api,
    "X-RapidAPI-Host": "api-football-v1.p.rapidapi.com"
}

query = {
    'season': '2022',
    'league': '140'
}

response = requests.get(url, headers=headers, params=query)

json_res = response.json()

rank_list = []
team_list = []
wins_list = []
draws_list = []
loses_list = []
points_list = []

count = 0
while count < 20:
    rank_list.append(int(json.dumps(json_res["response"][0]["league"]["standings"][0][count]["rank"])))
    team_list.append(str(json.dumps(json_res["response"][0]["league"]["standings"][0][count]["team"]["name"])))
    wins_list.append(int(json.dumps(json_res["response"][0]["league"]["standings"][0][count]["all"]["win"])))
    draws_list.append(int(json.dumps(json_res["response"][0]["league"]["standings"][0][count]["all"]["draw"])))
    loses_list.append(int(json.dumps(json_res["response"][0]["league"]["standings"][0][count]["all"]["lose"])))
    points_list.append(int(json.dumps(json_res["response"][0]["league"]["standings"][0][count]["points"])))
    count += 1

stripped_team = []
for team in team_list:
    team = team.strip('"')
    stripped_team.append(team)

class Standings:
    def drop(self):
        client = bigquery.Client(project=project_id)
        query = f"""
            DROP TABLE {project_id}.{dataset_id}.{table_name}
        """
        query_job = client.query(query)
        print("Table dropped...")

    def table(self):
        zipped = list(zip(rank_list, stripped_team, wins_list, draws_list, loses_list, points_list))

        df = pd.DataFrame(zipped, columns=['Rank', 'Team', 'Wins', 'Draws', 'Loses', 'Points'])

        client = bigquery.Client(project=project_id)

        table_id = f'{project_id}.{dataset_id}.{table_name}'

        job = client.load_table_from_dataframe(
            df, table_id
        )

        job.result()

        table = client.get_table(table_id)

        print(f"Loaded {table.num_rows} and {len(table.schema)}")