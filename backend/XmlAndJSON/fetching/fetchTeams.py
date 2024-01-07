import requests
import json

def fetch_all_teams_data(api_endpoint):
    response = requests.get(api_endpoint)
    if response.status_code == 200:
        teams = response.json()['data']
        teams = teams[:1000]  # Limit to 1000 teams if necessary
        return teams
    else:
        print(f"Failed to fetch data. Status code: {response.status_code}")
        return []
