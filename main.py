from flask import Flask, jsonify
from v99_engine import build_bet
from data_provider import get_matches
from odds_provider import get_live_odds
from datetime import datetime
import os

app = Flask(__name__)

def normalize(name):
    return (
        name.lower()
        .replace("fc", "")
        .replace("cf", "")
        .replace(".", "")
        .replace("club", "")
        .strip()
    )

@app.route("/")
def home():
    return jsonify({
        "system": "SMART BETTING LAB V99.8",
        "status": "REALISTIC FILTERED ENGINE",
        "time": datetime.utcnow().isoformat()
    })

@app.route("/portfolio")
def portfolio():
    raw_matches = get_matches()
    live_odds = get_live_odds()

    # ✅ Match odds properly
    for m in raw_matches:
        home, away = m["match"].split(" vs ")
        home_n = normalize(home)
        away_n = normalize(away)

        for lo in live_odds:
            lo_home, lo_away = lo["match"].split(" vs ")
            lo_home_n = normalize(lo_home)
            lo_away_n = normalize(lo_away)

            if (
                (home_n in lo_home_n or lo_home_n in home_n)
                and (away_n in lo_away_n or lo_away_n in away_n)
            ):
                m["odds"] = lo["odds"]

    bets = []

    for m in raw_matches:
        base = m["model_probability"]

        market_space = [
            ("OVER_2.5", base),
            ("UNDER_2.5", 1 - base),

            ("BTTS_YES", base * 0.9),
            ("BTTS_NO", 1 - (base * 0.9)),

            ("HOME_WIN", 0.45),
            ("DRAW", 0.25),
            ("AWAY_WIN", 0.30),
        ]

        best_bet = None

        for market_name, prob in market_space:
            m_copy = m.copy()
            m_copy["market"] = market_name
            m_copy["model_probability"] = round(max(0.05, min(0.95, prob)), 2)

            bet = build_bet(m_copy)

            # ✅ STRICT FILTER
            if bet["edge"] > 0.03 and bet["odds"] != 2:
                if best_bet is None or bet["edge"] > best_bet["edge"]:
                    best_bet = bet

        if best_bet:
            bets.append(best_bet)

    return jsonify({
        "system": "SMART BETTING LAB V99.8",
        "bets": bets,
        "count": len(bets)
    })

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
