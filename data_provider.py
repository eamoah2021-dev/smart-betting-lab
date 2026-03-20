import requests
import datetime

API_KEY = "59014f39c8de466b8381d0bd3ffe12a4"

def get_matches():
    url = "https://api.football-data.org/v4/matches"
    headers = {"X-Auth-Token": API_KEY}
    try:
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            print("API ERROR:", response.status_code)
            return []

        data = response.json()
        matches = []

        for m in data.get("matches", []):
            # Dynamic probability heuristic:
            # If kickoff is today, assign probability between 0.5–0.7
            model_prob = 0.55
            try:
                kickoff = datetime.datetime.fromisoformat(m["utcDate"].replace("Z",""))
                today = datetime.datetime.utcnow()
                if abs((kickoff - today).days) <= 7:
                    model_prob = 0.55 + 0.05  # increase for near matches
            except:
                pass

            matches.append({
                "league": m["competition"]["name"],
                "match": f'{m["homeTeam"]["name"]} vs {m["awayTeam"]["name"]}',
                "market": "OVER_2.5",
                "odds": 2.0,  # will be replaced by live odds
                "model_probability": model_prob,
                "kickoff": m["utcDate"]
            })
        return matches
    except Exception as e:
        print("ERROR:", str(e))
        return []
