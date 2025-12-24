import time
import random
import yfinance as yf
from database import FinanceDAO

#Fake Stock used to show the app updates correctly
class FakeStock:
    def __init__(self, symbol, start_price):
        self.symbol = symbol
        self.price = start_price
        self.history = []
    
    def update(self):
        # Random walk: price changes by -1% to +1%
        change_pct = random.uniform(-0.01, 0.01)
        self.price *= (1 + change_pct)
        self.history.append(self.price)
        
        # Keep only last 5 entries for moving average
        if len(self.history) > 5:
            self.history.pop(0)
            
        mavg_5min = sum(self.history) / len(self.history)
        
        return {
            "price": self.price,
            "mavg_5min": mavg_5min,
            "change_pct": change_pct * 100
        }

def fetch_and_store_data():
    dao = FinanceDAO()
    # Ensure FAKE ticker is in the watchlist so it appears in the dashboard
    dao.add_watched_ticker("FAKE")
    fake_stock = FakeStock("FAKE", 100.00)
    print("Starting data ingestion loop (Ctrl+C to stop)...")
    
    while True:
        try:
            # 0. list of Tickers from DB
            real_tickers = dao.get_watched_tickers()

            # 1. Process Tickers
            for symbol in real_tickers:
                try:
                    ticker = yf.Ticker(symbol)
                    hist = ticker.history(period="1d", interval="1m")
                    
                    if not hist.empty:
                        current_price = hist['Close'].iloc[-1]
                        
                        if len(hist) >= 5:
                            mavg_5min = hist['Close'].tail(5).mean()
                        else:
                            mavg_5min = current_price
                            
                        open_price = hist['Open'].iloc[-1]
                        change_pct = ((current_price - open_price) / open_price) * 100
                        change_str = f"{change_pct:+.2f}%"
                        
                        print(f"Updating {symbol}: ${current_price:.2f} | 5m Avg: ${mavg_5min:.2f} | Change: {change_str}")
                        
                        dao.insert_metric(symbol, float(current_price), float(mavg_5min), change_str)
                except Exception as e:
                    print(f"Failed to fetch {symbol}: {e}")

            # 2. Process Fake Ticker
            data = fake_stock.update()
            change_str = f"{data['change_pct']:+.2f}%"
            print(f"Updating {fake_stock.symbol}: ${data['price']:.2f} | 5m Avg: ${data['mavg_5min']:.2f} | Change: {change_str}")
            
            dao.insert_metric(
                fake_stock.symbol, 
                float(data['price']), 
                float(data['mavg_5min']),
                change_str
            )
            
            print("Update complete. Waiting 10 seconds...")
            time.sleep(10)
            
        except Exception as e:
            print(f"Error occurred: {e}")
            time.sleep(10)

if __name__ == "__main__":
    fetch_and_store_data()
