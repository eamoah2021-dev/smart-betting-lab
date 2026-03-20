import requests

API_KEY = "3865c7e02e8dc75071e87271b92316f1"

def get_live_odds():
    url = f"https://api.the-odds-api.com/v4/sports/soccer_epl/odds/?apiKey={API_KEY}&regions=eu&markets=totals&oddsFormat=decimal"

    try:
        response = requests.get(url)
        if response.status_code != 200:
            return []

        data = response.json()
        odds_list = []

        for match in data:
            try:
                home = match["home_team"]
                away = match["away_team"]

                odds_value = None

                for bookmaker in match.get("bookmakers", []):
                    for market in bookmaker.get("markets", []):
                        if market["key"] == "totals":
                            for outcome in market.get("outcomes", []):
                                if outcome["name"] == "Over 2.5":
                                    odds_value = outcome["price"]

                if odds_value:
                    odds_list.append({
                        "match": f"{home} vs {away}",
                        "odds": odds_value
                    })

            except:
                continue

        return odds_list

    except Exception as e:
        print("ERROR:", str(e))
        return []
