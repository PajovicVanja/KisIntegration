import requests
import json
import time

def fetch_all_players_data(base_url, max_players=1000):
    all_players = []
    page = 0
    while True:
        url = f"{base_url}?page={page}"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            players = data['data']
            if not players:
                break  # No more players found, exit the loop
            for player in players:
                if 'team' in player:
                    player['teamID'] = player['team']['id']
                    del player['team']
            all_players.extend(players)
            if len(all_players) >= max_players:
                break  # Reached the max player limit, exit the loop
            page += 1
            # time.sleep(1)  # Sleep to avoid hitting API rate limits
        else:
            print(f"Failed to fetch data for page {page}. Status code: {response.status_code}")
            break
    return all_players[:max_players]
