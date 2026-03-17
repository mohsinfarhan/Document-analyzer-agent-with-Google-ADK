import os
import requests
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("ALPHA_VANTAGE_KEY")

def get_stock_price(symbol: str) -> str:
    """
    Fetches the real-time stock price for a given ticker symbol using Alpha Vantage.
    """
    url = "https://www.alphavantage.co/query"
    params = {
        "function": "GLOBAL_QUOTE",
        "symbol": symbol.upper(),
        "apikey": API_KEY
    }
    
    try:
        response = requests.get(url, params=params)
        data = response.json()
        
        # Check for Alpha Vantage API errors or rate limits
        if "Note" in data:
            return "API Rate limit reached. Please try again in a minute."
        
        quote = data.get("Global Quote", {})
        price = quote.get("05. price")
        
        if price:
            formatted_price = f"{float(price):.2f}"
            return f"The current stock price of {symbol.upper()} is ${formatted_price}."
        
        return f"Ticker symbol '{symbol}' not found or no data available."
        
    except Exception as e:
        return f"Error connecting to Stock API: {str(e)}"

# Direct test execution
if __name__ == "__main__":
    # Test with Tesla
    print(get_stock_price("TSLA"))