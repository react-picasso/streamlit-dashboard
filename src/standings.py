from config import rapid_api, standings_name, dataset_id, project_id
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
goals_for = []
goals_against = []
goals_diff = []

count = 0
while count < 20:
    rank_list.append(int(json.dumps(json_res["response"][0]["league"]["standings"][0][count]["rank"])))
    team_list.append(str(json.dumps(json_res["response"][0]["league"]["standings"][0][count]["team"]["name"])).strip('"'))
    wins_list.append(int(json.dumps(json_res["response"][0]["league"]["standings"][0][count]["all"]["win"])))
    draws_list.append(int(json.dumps(json_res["response"][0]["league"]["standings"][0][count]["all"]["draw"])))
    loses_list.append(int(json.dumps(json_res["response"][0]["league"]["standings"][0][count]["all"]["lose"])))
    points_list.append(int(json.dumps(json_res["response"][0]["league"]["standings"][0][count]["points"])))
    goals_for.append(int(json.dumps(json_res["response"][0]["league"]["standings"][0][count]["all"]["goals"]["for"])))
    goals_against.append(int(json.dumps(json_res["response"][0]["league"]["standings"][0][count]["all"]["goals"]["against"])))
    goals_diff.append(int(json.dumps(json_res["response"][0]["league"]["standings"][0][count]["goalsDiff"])))
    count += 1

class Standings:
    def drop(self):
        client = bigquery.Client(project=project_id)
        query = f"""
            DROP TABLE {project_id}.{dataset_id}.{standings_name}
        """
        query_job = client.query(query)
        print("Standings table dropped...")

    def table(self):
        zipped = list(zip(rank_list, team_list, wins_list, draws_list, loses_list, points_list, goals_for, goals_against, goals_diff))

        df = pd.DataFrame(zipped, columns=['Rank', 'Team', 'Wins', 'Draws', 'Loses', 'Points', 'GF', 'GA', 'GD'])

        client = bigquery.Client(project=project_id)

        table_id = f'{project_id}.{dataset_id}.{standings_name}'

        job = client.load_table_from_dataframe(
            df, table_id
        )

        job.result()

        table = client.get_table(table_id)

        print(f"Loaded {table.num_rows} and {len(table.schema)}")