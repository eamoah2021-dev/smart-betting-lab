# v100_engine.py
import datetime
import random

# Sample betting markets; in real use, fetch dynamically from an API
ALL_MARKETS = [
    "HOME_WIN", "DRAW", "AWAY_WIN",
    "OVER_0.5", "OVER_1.5", "OVER_2.5", "OVER_3.5",
    "UNDER_0.5", "UNDER_1.5", "UNDER_2.5", "UNDER_3.5",
    "BTTS_YES", "BTTS_NO"
]

# Sample tiers for betting confidence
def assign_tier(confidence):
    if confidence >= 0.6:
        return "TIER1"
    elif confidence >= 0.55:
        return "TIER2"
    else:
        return "TIER3"

def calculate_kelly_fraction(edge):
    # Use half Kelly for safer staking
    return round(max(edge * 0.5, 0.01), 2)

def build_bets(bankroll=100, leagues=None, markets=None):
    """
    Build a smart betting portfolio.
    :param bankroll: total bankroll
    :param leagues: list of leagues to filter, empty = all
    :param markets: list of markets to filter, empty = all
    :return: list of bets
    """
    # Sample matches; replace with real live matches from API
    sample_matches = [
        {"league": "Premier League", "home": "Manchester City FC", "away": "Crystal Palace FC"},
        {"league": "Serie A", "home": "Genoa CFC", "away": "Udinese Calcio"},
        {"league": "Bundesliga", "home": "RB Leipzig", "away": "TSG 1899 Hoffenheim"},
        {"league": "Campeonato Brasileiro Série A", "home": "Chapecoense AF", "away": "SC Corinthians Paulista"},
        {"league": "Eredivisie", "home": "Heracles Almelo", "away": "SBV Excelsior"}
    ]

    bets = []
    now = datetime.datetime.utcnow().isoformat()

    # Use all markets if none provided
    markets_to_use = markets if markets else ALL_MARKETS

    # Use all leagues if none provided
    leagues_to_use = leagues if leagues else [m["league"] for m in sample_matches]

    for match in sample_matches:
        if match["league"] not in leagues_to_use:
            continue

        for market in markets_to_use:
            # Simulate probability model; replace with real model later
            model_prob = round(random.uniform(0.5, 0.7), 2)
            implied_prob = 1 / 2  # Assuming odds = 2 for sample
            edge = round(model_prob - implied_prob, 2)
            if edge <= 0:
                continue  # Skip negative edge

            kelly = calculate_kelly_fraction(edge)
            stake = round(bankroll * kelly, 2)
            confidence = round(model_prob, 2)
            tier = assign_tier(confidence)

            bet = {
                "confidence": confidence,
                "created_at": now,
                "edge": edge,
                "implied_probability": implied_prob,
                "kelly_fraction": kelly,
                "league": match["league"],
                "market": market,
                "match": f"{match['home']} vs {match['away']}",
                "match_id": f"{random.randint(1000000000,9999999999)}",
                "model_probability": model_prob,
                "odds": 2,  # replace with real odds later
                "stake": stake,
                "status": "PENDING",
                "tier": tier
            }
            bets.append(bet)

    # Sort by edge descending to prioritize best value bets
    bets.sort(key=lambda x: x["edge"], reverse=True)
    return bets
