import yfinance as yf

class MarketDataService:
    @staticmethod
    def get_historical_bars(symbol: str, period: str = "1mo", interval: str = "1d"):
        """Fetch historical OHLCV data using yfinance."""
        ticker = yf.Ticker(symbol)
        df = ticker.history(period=period, interval=interval)
        
        # Convert to a list of dicts suitable for charting libraries
        bars = []
        for index, row in df.iterrows():
            bars.append({
                "time": index.strftime('%Y-%m-%d'),
                "open": row["Open"],
                "high": row["High"],
                "low": row["Low"],
                "close": row["Close"],
                "volume": row["Volume"]
            })
        return bars

    @staticmethod
    def get_quote(symbol: str):
        """Fetch a single delayed quote."""
        ticker = yf.Ticker(symbol)
        info = ticker.fast_info
        return {
            "symbol": symbol,
            "last_price": info.last_price,
            "previous_close": info.previous_close
        }
