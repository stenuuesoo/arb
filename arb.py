import ccxt
import time

api_key = "G62qJGvkp5QqJRL32jSKZuwsiOEcwF9GpOoLuUs4p1WlwGPdgwOJdPX509AxISoR"
api_secret = "nf4yugs3akURKcleY67hMTo9mqYGqHM50NtEGXFHeub7nEUXX518nHnciFi0zaVZ"

binance = ccxt.binance({
    "apiKey": api_key,
    "secret": api_secret,
})

def arbitrage(symbol1, symbol2, threshold=0.01):
    while True:
        try:
            ticker1 = binance.fetch_ticker(symbol1)
            ticker2 = binance.fetch_ticker(symbol2)

            bid1 = ticker1['bid']
            ask1 = ticker1['ask']
            bid2 = ticker2['bid']
            ask2 = ticker2['ask']

            if bid1 / ask2 > 1 + threshold:
                print(f"Arbitrage opportunity: Buy {symbol2} and sell {symbol1}")
                print(f"Buy price: {ask2}, Sell price: {bid1}")

            if bid2 / ask1 > 1 + threshold:
                print(f"Arbitrage opportunity: Buy {symbol1} and sell {symbol2}")
                print(f"Buy price: {ask1}, Sell price: {bid2}")

        except Exception as e:
            print(f"Error: {e}")

        time.sleep(5)

if __name__ == "__main__":
    # Replace 'BTC/USDT' and 'ETH/USDT' with the trading pairs you want to monitor.
    arbitrage("BTC/USDT", "ETH/USDT", threshold=0.01)
