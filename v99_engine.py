from datetime import datetime
import uuid

def calculate_implied_probability(odds):
    return 1 / odds

def kelly_fraction(prob, odds):
    b = odds - 1
    return max((b * prob - (1 - prob)) / b, 0)

def classify_tier(edge, confidence):
    if edge > 0.08 and confidence > 0.80:
        return "TIER1"
    elif edge > 0.05:
        return "TIER2"
    else:
        return "TIER3"

def build_bet(match_data):
    model_prob = match_data["model_probability"]
    odds = match_data["odds"]

    implied = calculate_implied_probability(odds)
    edge = model_prob - implied
    kelly = kelly_fraction(model_prob, odds)

    confidence = min(0.95, model_prob + edge)
    tier = classify_tier(edge, confidence)

    return {
        "match_id": str(uuid.uuid4()),
        "league": match_data.get("league", "Unknown"),
        "match": match_data["match"],
        "market": match_data["market"],
        "odds": odds,
        "model_probability": round(model_prob, 3),
        "implied_probability": round(implied, 3),
        "edge": round(edge, 3),
        "confidence": round(confidence, 3),
        "tier": tier,
        "stake": round(kelly * 10, 2),
        "kelly_fraction": round(kelly, 3),
        "status": "PENDING",
        "created_at": datetime.utcnow().isoformat()
    }
