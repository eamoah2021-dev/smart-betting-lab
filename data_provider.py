import requests

API_KEY = "YOUR_API_KEY_HERE"

def get_matches():
    url = "https://api.football-data.org/v4/matches"

    headers = {
        "X-Auth-Token": API_KEY
    }

    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        return []

    data = response.json()

    matches = []

    for m in data.get("matches", []):
        matches.append({
            "league": m["competition"]["name"],
            "match": f'{m["homeTeam"]["name"]} vs {m["awayTeam"]["name"]}',
            "market": "OVER_2.5",
            "odds": 2.0,  # placeholder for now
            "model_probability": 0.55,  # temporary
            "kickoff": m["utcDate"]
        })

    return matches
