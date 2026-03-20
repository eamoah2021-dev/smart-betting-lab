from flask import Flask, jsonify
from v99_engine import build_bet
from data_provider import get_matches
from datetime import datetime
import os

app = Flask(__name__)

@app.route("/")
def home():
    return jsonify({
        "system": "SMART BETTING LAB V99.2",
        "status": "LIVE DATA MODE",
        "time": datetime.utcnow().isoformat()
    })

@app.route("/portfolio")
def portfolio():
    raw_matches = get_matches()

    bets = []
    for m in raw_matches:
        bets.append(build_bet(m))

    return jsonify({
        "system": "SMART BETTING LAB V99.2",
        "bets": bets,
        "count": len(bets)
    })

# ✅ THIS PART MUST BE CLEAN AND SEPARATE
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
