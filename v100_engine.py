# v100_engine.py
from datetime import datetime
import random

# Simulated leagues and matches (replace with real odds API in production)
LEAGUES = {
    "Premier League": ["Manchester City FC vs Crystal Palace FC", "AFC Bournemouth vs Manchester United FC"],
    "Serie A": ["Cagliari Calcio vs SSC Napoli", "Genoa CFC vs Udinese Calcio"],
    "Bundesliga": ["RB Leipzig vs TSG 1899 Hoffenheim"],
    "Ligue 1": ["Racing Club de Lens vs Angers SCO"],
    "Championship": ["Preston North End FC vs Stoke City FC"],
    "Primeira Liga": ["CF Estrela da Amadora vs Casa Pia AC"],
    "Eredivisie": ["Heracles Almelo vs SBV Excelsior"],
    "Campeonato Brasileiro Série A": ["Chapecoense AF vs SC Corinthians Paulista"],
    "Primera Division": ["Villarreal CF vs Real Sociedad de Fútbol"]
}

# All markets to consider
MARKETS = ["HOME_WIN", "DRAW", "AWAY_WIN", "OVER_2.5", "UNDER_2.5", "BTTS_YES", "BTTS_NO"]

# Sample bankroll
BANKROLL = 10  # can be dynamic

def build_bets():
    """
    Build smart value bets across all leagues and markets
    """
    bets = []

    for league, matches in LEAGUES.items():
        for match in matches:
            for market in MARKETS:
                # simulate model probability intelligently
                model_probability = round(random.uniform(0.45, 0.75), 2)
                odds = 2  # placeholder: replace with real odds API
                implied_probability = round(1 / odds, 2)
                edge = round((model_probability * odds) - 1, 2)

                # Only include positive edge bets
                if edge > 0.03:
                    kelly_fraction = round(edge / (odds - 1), 2)
                    stake = round(kelly_fraction * BANKROLL, 2)
                    confidence = model_probability

                    bet = {
                        "confidence": confidence,
                        "created_at": datetime.utcnow().isoformat(),
                        "edge": edge,
                        "implied_probability": implied_probability,
                        "kelly_fraction": kelly_fraction,
                        "league": league,
                        "market": market,
                        "match": match,
                        "match_id": f"{hash(match + market) % 10**16}",
                        "model_probability": model_probability,
                        "odds": odds,
                        "stake": stake,
                        "status": "PENDING",
                        "tier": "TIER1" if edge > 0.1 else ("TIER2" if edge > 0.05 else "TIER3")
                    }
                    bets.append(bet)
    # Sort by edge descending
    bets.sort(key=lambda x: x["edge"], reverse=True)
    return bets
