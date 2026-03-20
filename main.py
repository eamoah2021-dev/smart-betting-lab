from flask import Flask, jsonify
from v99_engine import build_bet
from datetime import datetime
import os

app = Flask(__name__)

@app.route("/")
def home():
    return jsonify({
        "system": "SMART BETTING LAB V99.1",
        "status": "running",
        "time": datetime.utcnow().isoformat()
    })

@app.route("/portfolio")
def portfolio():
    raw_matches = [
        {
            "league": "Bundesliga",
            "match": "Augsburg vs FC Koln",
            "market": "OVER_2.5",
            "odds": 1.85,
            "model_probability": 0.64,
            "kickoff": "2026-03-21T14:30:00Z"
        }
    ]

    bets = []
    for m in raw_matches:
        bets.append(build_bet(m))

    return jsonify({
        "system": "SMART BETTING LAB V99.1",
        "bets": bets
    })

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
