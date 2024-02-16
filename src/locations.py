from config import locations_name, rapid_api, project_id, dataset_id
from google.cloud import bigquery
import pandas as pd
import requests
import json

url_standings = "https://api-football-v1.p.rapidapi.com/v3/standings"

query = {
    'season': '2022',
    'league': '140'
}

headers = {
    "X-RapidAPI-Key": rapid_api,
    "X-RapidAPI-Host": "api-football-v1.p.rapidapi.com"
}

response = requests.get(url_standings, headers=headers, params=query)

json_res = response.json()

id_list = []

count = 0

while count < 20:
    id_list.append(str(json.dumps(json_res["response"][0]["league"]["standings"][0][count]["team"]["id"])))
    count += 1

team_list = []
city_list = []

for id in id_list:
    query_string = {"id":id}

    url = "https://api-football-v1.p.rapidapi.com/v3/teams"

    response = requests.get(url, headers=headers, params=query_string)

    json_res = response.json()

    team_list.append(str(json.dumps(json_res["response"][0]["team"]["name"])))
    city_list.append(str(json.dumps(json_res["response"][0]["venue"]["city"])))

stripped_team = []

for team in team_list:
    team = team.strip('"')
    stripped_team.append(team)

stripped_city = []
for city in city_list:
    city = city.strip('"')
    city = city.split(',', 1)[0]
    stripped_city.append(city)

class Location:
    def drop(self):
        client = bigquery.Client(project=project_id)
        query = f"""
            DROP TABLE {project_id}.{dataset_id}.{locations_name}
        """
        query_job = client.query(query)
        print("Locations table dropped...")

    def table(self):
        headers = ['Team', 'City']
        zipped = list(zip(stripped_team, stripped_city))

        df = pd.DataFrame(zipped, columns=headers)

        client = bigquery.Client(project=project_id)

        table_id = f'{project_id}.{dataset_id}.{locations_name}'

        job = client.load_table_from_dataframe(df,  table_id)

        job.result()

        table = client.get_table(table_id)

        print(f"Loaded {table.num_rows} rows & {len(table.schema)} columns")