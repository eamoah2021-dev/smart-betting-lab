import requests

API_KEY = "59014f39c8de466b8381d0bd3ffe12a4"  # <- Replace with your real key

def get_live_odds():
    url = f"https://api.the-odds-api.com/v4/sports/soccer_epl/odds/?apiKey={API_KEY}&regions=eu&markets=totals&oddsFormat=decimal"

    try:
        response = requests.get(url)
        if response.status_code != 200:
            print("ODDS API ERROR:", response.status_code)
            return []

        data = response.json()
        odds_list = []

        for match in data:
            try:
                home = match["home_team"]
                away = match["away_team"]
                total_odds = None
                for bookmaker in match.get("bookmakers", []):
                    for market in bookmaker.get("markets", []):
                        if market["key"] == "totals":
                            for outcome in market.get("outcomes", []):
                                if outcome["name"] == "Over 2.5":
                                    total_odds = outcome["price"]
                if total_odds:
                    odds_list.append({
                        "match": f"{home} vs {away}",
                        "odds": total_odds
                    })
            except:
                continue

        return odds_list

    except Exception as e:
        print("ERROR FETCHING ODDS:", str(e))
        return []
