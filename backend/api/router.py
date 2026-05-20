from fastapi import APIRouter
from pydantic import BaseModel
from typing import List

router = APIRouter()

class TickerInfo(BaseModel):
    symbol: str
    name: str

@router.get("/tickers", response_model=List[TickerInfo])
async def get_popular_tickers():
    """Mock endpoint to return a list of popular tickers for search autocomplete."""
    return [
        {"symbol": "AAPL", "name": "Apple Inc."},
        {"symbol": "MSFT", "name": "Microsoft Corp."},
        {"symbol": "TSLA", "name": "Tesla Inc."},
        {"symbol": "NVDA", "name": "NVIDIA Corp."},
        {"symbol": "SPY", "name": "SPDR S&P 500 ETF"},
    ]
