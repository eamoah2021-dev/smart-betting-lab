from flask import Flask, jsonify
from v99_engine import build_bet
from datetime import datetime
import os

# Initialize Flask app
app = Flask(__name__)

# -------------------------------
# Health Check Route
# -------------------------------
@app.route("/")
def home():
    return jsonify({
        "system": "SMART BETTING LAB V99.1",
        "status": "Backend is running",
        "timestamp": datetime.utcnow().isoformat()
    })

# -------------------------------
# Portfolio Route
# -------------------------------
@app.route("/portfolio")
def portfolio():
    # Example matches (replace with live data later)
    raw_matches = [
        {
            "league": "Bundesliga",
            "match": "Augsburg vs FC Koln",
            "market": "OVER_2.5",
            "odds": 1.85,
            "model_probability": 0.64,
            "kickoff": "2026-03-21T14:30:00Z"
        },
        {
            "league": "Premier League",
            "match": "Manchester United vs Arsenal",
            "market": "OVER_2.5",
            "odds": 1.95,
            "model_probability": 0.62,
            "kickoff": "2026-03-22T16:00:00Z"
        }
    ]

    # Build professional bets
    bets = [build_bet(m) for m in raw_matches]

    return jsonify({
        "system": "SMART BETTING LAB V99.1",
        "bets": bets,
        "generated_at": datetime.utcnow().isoformat()
    })

# -------------------------------
# Run Flask with Render port
# -------------------------------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host="0.0.0.0", port=port)
