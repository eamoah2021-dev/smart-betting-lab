from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from v99_engine import generate_portfolio

app = FastAPI()

# Enable frontend access (VERY IMPORTANT)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {"message": "SMART BETTING LAB V99 API LIVE"}

@app.get("/portfolio")
def portfolio():
    return generate_portfolio()