import datetime

def build_bet(match):
    odds = match.get("odds", 2.0)
    prob = match.get("model_probability", 0.55)

    implied_prob = 1 / odds
    edge = prob - implied_prob

    # Kelly formula
    kelly_fraction = 0
    if edge > 0:
        kelly_fraction = edge / (odds - 1)
        kelly_fraction = round(min(kelly_fraction, 1), 3)

    # Confidence heuristic
    confidence = round(prob, 2)

    # Tier classification
    if edge >= 0.08:
        tier = "TIER1"
    elif edge >= 0.04:
        tier = "TIER2"
    else:
        tier = "TIER3"

    return {
        "match_id": str(datetime.datetime.utcnow().timestamp()).replace(".", ""),
        "match": match["match"],
        "league": match["league"],
        "market": match["market"],
        "odds": odds,
        "model_probability": prob,
        "implied_probability": round(implied_prob, 3),
        "edge": round(edge, 3),
        "kelly_fraction": kelly_fraction,
        "stake": round(kelly_fraction * 10, 2),  # Example bankroll = 10 units
        "confidence": confidence,
        "status": "PENDING",
        "tier": tier,
        "created_at": datetime.datetime.utcnow().isoformat()
    }        "implied_probability": round(implied, 3),
        "edge": round(edge, 3),
        "confidence": round(confidence, 3),
        "tier": tier,
        "stake": round(kelly * 10, 2),
        "kelly_fraction": round(kelly, 3),
        "status": "PENDING",
        "created_at": datetime.utcnow().isoformat()
    }
