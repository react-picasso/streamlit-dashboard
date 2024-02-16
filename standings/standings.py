from config import rapid_api
import pandas as pd
import requests
import json
import matplotlib.pyplot as plt

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

class Standings:
    def table(self):
        zipped = list(zip(rank_list, team_list, wins_list, draws_list, loses_list, points_list))

        df = pd.DataFrame(zipped, columns=['Rank', 'Team', 'Wins', 'Draws', 'Loses', 'Points'])

    def graph(self):
        df_graph = pd.DataFrame({
            'Points': points_list,
            'Wins': wins_list,
            'Draws': draws_list
            }, index=team_list)

        ax = df_graph.plot.bar(rot=45)
        plt.show()