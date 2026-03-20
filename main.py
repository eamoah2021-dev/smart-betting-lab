# main.py
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from v100_engine import build_bets  # Updated to V100 engine
from pydantic import BaseModel
from typing import List

app = FastAPI(title="SMART BETTING LAB API V100")

# CORS settings (allow all origins for testing; restrict in production)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request model for portfolio parameters
class PortfolioRequest(BaseModel):
    bankroll: float
    leagues: List[str] = []
    markets: List[str] = []  # Include all markets, not just over 2.5

# Response model for bets
class BetResponse(BaseModel):
    confidence: float
    edge: float
    implied_probability: float
    kelly_fraction: float
    league: str
    market: str
    match: str
    match_id: str
    model_probability: float
    odds: float
    stake: float
    status: str
    tier: str
    created_at: str

@app.post("/portfolio", response_model=List[BetResponse])
def portfolio(request: PortfolioRequest):
    """
    Build and return betting portfolio.
    Uses V100 engine for smart bet selection.
    """
    try:
        bets = build_bets(
            bankroll=request.bankroll,
            leagues=request.leagues,
            markets=request.markets  # Pass all requested markets
        )
        return bets
    except Exception as e:
        return {"error": str(e)}

# Optional health check endpoint
@app.get("/health")
def health():
    return {"status": "OK", "system": "SMART BETTING LAB V100"}

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
