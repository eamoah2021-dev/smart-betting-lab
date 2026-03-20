import requests
import random

API_KEY = "YOUR_FOOTBALL_DATA_API_KEY_HERE"

def get_matches():
    url = "https://api.football-data.org/v4/matches"
    headers = {"X-Auth-Token": API_KEY}

    try:
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            return []

        data = response.json()
        matches = []

        for m in data.get("matches", []):
            home = m["homeTeam"]["name"]
            away = m["awayTeam"]["name"]

            # 🔥 SIMPLE SCORING MODEL
            # Instead of fixed 0.6, create realistic variation
            base = 0.48  # market baseline for over 2.5

            # random small variation to simulate team differences
            variation = random.uniform(-0.08, 0.12)

            model_prob = round(max(0.35, min(0.75, base + variation)), 2)

            matches.append({
                "league": m["competition"]["name"],
                "match": f"{home} vs {away}",
                "market": "OVER_2.5",
                "odds": 2.0,
                "model_probability": model_prob,
                "kickoff": m["utcDate"]
            })

        return matches

    except Exception as e:
        print("ERROR:", str(e))
        return []
