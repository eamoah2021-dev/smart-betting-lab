import requests

API_KEY = "59014f39c8de466b8381d0bd3ffe12a4"

def get_matches():
    url = "https://api.football-data.org/v4/matches"

    headers = {
        "X-Auth-Token": API_KEY
    }

    try:
        response = requests.get(url, headers=headers)

        if response.status_code != 200:
            print("API ERROR:", response.status_code)
            return []

        data = response.json()

        matches = []

        for m in data.get("matches", []):
            matches.append({
                "league": m["competition"]["name"],
                "match": f'{m["homeTeam"]["name"]} vs {m["awayTeam"]["name"]}',
                "market": "OVER_2.5",
                "odds": 2.0,
                "model_probability": 0.55,
                "kickoff": m["utcDate"]
            })

        return matches

    except Exception as e:
        print("ERROR:", str(e))
        return []
