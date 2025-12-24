import pandas as pd
from sqlalchemy import create_engine, text

class FinanceDAO:
    def __init__(self):
        # Connection string matching docker-compose
        self.engine = create_engine('postgresql://admin:password123@localhost:5432/finance_db')

    def get_latest_metrics(self):
        """Fetch the latest record for each ticker for the dashboard."""
        query = """
            SELECT DISTINCT ON (m.ticker) m.*
            FROM market_metrics m
            JOIN watched_tickers w ON m.ticker = w.symbol
            ORDER BY m.ticker, m.Datetime DESC
        """
        return pd.read_sql(query, self.engine)

    def insert_metric(self, ticker, price, mavg_5min, price_change):
        """Insert a new market metric record."""
        with self.engine.begin() as conn:
            query = text("""
                INSERT INTO market_metrics (ticker, price, mavg_5min, price_change)
                VALUES (:ticker, :price, :mavg_5min, :price_change)
            """)
            conn.execute(query, {
                "ticker": ticker,
                "price": price,
                "mavg_5min": mavg_5min,
                "price_change": price_change
            })

    def get_watched_tickers(self):
        """Get list of symbols to track."""
        query = "SELECT symbol FROM watched_tickers"
        df = pd.read_sql(query, self.engine)
        return df['symbol'].tolist()

    def add_watched_ticker(self, symbol):
        """Add a new ticker to the watch list."""
        with self.engine.begin() as conn:
            query = text("INSERT INTO watched_tickers (symbol) VALUES (:symbol) ON CONFLICT DO NOTHING")
            conn.execute(query, {"symbol": symbol.upper()})

    def remove_watched_ticker(self, symbol):
        """Remove a ticker from the watch list."""
        with self.engine.begin() as conn:
            query = text("DELETE FROM watched_tickers WHERE symbol = :symbol")
            conn.execute(query, {"symbol": symbol.upper()})
