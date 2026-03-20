import datetime

def build_bet(match):
    odds = match.get("odds", 2.0)
    prob = match.get("model_probability", 0.5)

    implied_prob = 1 / odds
    edge = prob - implied_prob

    # Kelly
    kelly_fraction = 0
    if edge > 0:
        kelly_fraction = edge / (odds - 1)
        kelly_fraction = round(min(kelly_fraction, 1), 3)

    confidence = round(prob, 2)

    # Tier system
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
        "stake": round(kelly_fraction * 10, 2),
        "confidence": confidence,
        "status": "PENDING",
        "tier": tier,
        "created_at": datetime.datetime.utcnow().isoformat()
    }
