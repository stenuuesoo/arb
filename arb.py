import ccxt
import time

api_key = "G62qJGvkp5QqJRL32jSKZuwsiOEcwF9GpOoLuUs4p1WlwGPdgwOJdPX509AxISoR"
api_secret = "nf4yugs3akURKcleY67hMTo9mqYGqHM50NtEGXFHeub7nEUXX518nHnciFi0zaVZ"

binance = ccxt.binance({
    "apiKey": api_key,
    "secret": api_secret,
})

def triangular_arbitrage(symbols, threshold=0.01):
    trading_fee = 0.001  # Binance trading fee (0.1%)
    sleep_interval = 5  # Time interval between checks in seconds
    print_interval = 30  # Time interval between printing threshold in seconds

    print("Serving script... ")

    counter = 0  # Initialize counter

    while True:
        try:
            tickers = {}
            for symbol in symbols:
                tickers[symbol] = binance.fetch_ticker(symbol)

            # Print ticker data for debugging
            print("Ticker data:", tickers)

            # Calculate arbitrage opportunity
            arb1 = (1 / tickers[symbols[0]]['ask']) * tickers[symbols[2]]['bid'] * tickers[symbols[1]]['bid']
            arb2 = (1 / tickers[symbols[1]]['ask']) * tickers[symbols[0]]['bid'] * tickers[symbols[2]]['ask']
            
            # Print intermediate values for debugging
            print(f"arb1: {arb1}, arb2: {arb2}")
            
            if arb1 > 1 + threshold:
                profit = arb1 * (1 - trading_fee) * (1 - trading_fee) - 1
                print(f"Arbitrage opportunity: Buy {symbols[1]} with {symbols[0]}, then buy {symbols[2]} with {symbols[1]}, and sell {symbols[2]} for {symbols[0]}.")
                print(f"Estimated profit (including fees): {profit * 100:.2f}%")
                print(f"arb1: {arb1}, trading_fee: {trading_fee}, profit: {profit}")

            if arb2 > 1 + threshold:
                profit = arb2 * (1 - trading_fee) * (1 - trading_fee) - 1
                print(f"Arbitrage opportunity: Buy {symbols[2]} with {symbols[0]}, then buy {symbols[1]} with {symbols[2]}, and sell {symbols[1]} for {symbols[0]}.")
                print(f"Estimated profit (including fees): {profit * 100:.2f}%")
                print(f"arb2: {arb2}, trading_fee: {trading_fee}, profit: {profit}")

            if counter * sleep_interval >= print_interval:
                print(f"Current threshold: {threshold * 100:.2f}%")
                counter = 0

        except Exception as e:
            print(f"Error: {e}")

        time.sleep(sleep_interval)
        counter += 1

if __name__ == "__main__":
    triangular_arbitrage(["BTC/USDT", "ETH/USDT", "ETH/BTC"], threshold=0.01)