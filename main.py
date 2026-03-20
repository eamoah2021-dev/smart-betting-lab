from flask import Flask, jsonify
from v99_engine import build_bet
from data_provider import get_matches
from odds_provider import get_live_odds
from datetime import datetime
import os

app = Flask(__name__)

@app.route("/")
def home():
    return jsonify({
        "system": "SMART BETTING LAB V99.5",
        "status": "LIVE + FILTERED EDGE MODE",
        "time": datetime.utcnow().isoformat()
    })

@app.route("/portfolio")
def portfolio():
    raw_matches = get_matches()
    live_odds = get_live_odds()

    # ✅ FUZZY MATCHING (FIXED)
    for m in raw_matches:
        home, away = m["match"].lower().split(" vs ")
        for lo in live_odds:
            lo_match = lo["match"].lower()
            if home in lo_match and away in lo_match:
                m["odds"] = lo["odds"]

    bets = []
    for m in raw_matches:
        bet = build_bet(m)

        # ✅ ONLY VALUE BETS
        if bet["edge"] > 0:
            bets.append(bet)

    return jsonify({
        "system": "SMART BETTING LAB V99.5",
        "bets": bets,
        "count": len(bets)
    })

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
