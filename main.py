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
        "system": "SMART BETTING LAB V99.4",
        "status": "LIVE ODDS + EDGE MODE",
        "time": datetime.utcnow().isoformat()
    })

@app.route("/portfolio")
def portfolio():
    raw_matches = get_matches()
    live_odds = get_live_odds()

    # Merge live odds
    for m in raw_matches:
        for lo in live_odds:
            if lo["match"] == m["match"]:
                m["odds"] = lo["odds"]

    bets = []
    for m in raw_matches:
        bets.append(build_bet(m))

    return jsonify({
        "system": "SMART BETTING LAB V99.4",
        "bets": bets,
        "count": len(bets)
    })

# ✅ CLEAN ENDING (NO EXTRA SYMBOLS)
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
