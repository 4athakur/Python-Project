from nsepython import nse_eq, nse_eq_symbols
import pywhatkit
import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
phone_number = "+918105749018"

official_symbol =[
    "NIFTYBEES",
    "BANKBEES",
    "JUNIORBEES",
    "GOLDBEES",
    "METALIETF",
    "SILVERBEES",
    "LIQUIDCASE",
    "ITBEES",
    "PHARMABEES",
    "PSUBNKBEES"
]
final = []
stock_name = {}
finallll = {}

for ii, i in enumerate(official_symbol):
    data = nse_eq(i)
    price_info = data.get('priceInfo', {})
    last_price = price_info.get('lastPrice')
    if last_price is None:
        print(f"{i}: No lastPrice available, skipping")
        continue
    final.append(last_price)
    stock_name.update({data['info']['companyName']: {i: last_price}})
    finallll.update({i: last_price})
difference = {}
for i in official_symbol:
    data = nse_eq(i)
    price_info = data.get('priceInfo', {})
    current_market_price = price_info.get('lastPrice')
    inav_price = price_info.get('iNavValue')
    if current_market_price is None or inav_price is None:
        print(f"{i}: Missing price data, skipping")
        continue
    inav_price = float(inav_price)
    diff = current_market_price - inav_price
    diff_percentage = (diff / current_market_price) * 100
    difference.update({i: diff_percentage})
    print(f"{i}: CMP={current_market_price}, iNAV={inav_price}, Diff%={diff_percentage:.2f}")

info = pd.DataFrame(list(difference.items()), columns=["Stock", "Slippage Difference"])

# Send nicely formatted DataFrame as WhatsApp message
ask=input("Would you like to get Today's Stock recommedation y\\n")
if(ask=='y'):
    pywhatkit.sendwhatmsg_instantly(phone_number, info.to_string())

#------------------------------------------ Secon Feature----------------------------------------------------
DAYS = 10  
# FETCH + DISPLAY LOGIC

def fetch_and_plot_stocks(symbols, days=DAYS):
    for sym in symbols:
        ticker = f"{sym}.NS"
        print(f"\nFetching {days}-day data for {sym}...")
        try:
            # Download daily data for the last 30 days
            df = yf.download(
                ticker,
                period=f"{days}d",
                interval="1d",
                auto_adjust=False,
                progress=False
            )
            # If no data returned, skip this symbol
            if df.empty:
                print(f"[WARN] No data for {sym}. Skipping.")
                continue
            # Reset index for easy plot
            df = df.reset_index()
            # Plot closing prices using pandas
            df.plot(
                x="Date",
                y="Close",
                title=f"{sym} - Last {days} Days Price Trend",
                ylabel="Price (₹)",
                xlabel="Date",
                legend=False,
                grid=True,
                figsize=(10, 5)
            )
            plt.show()  # show graph for each stock
        except Exception as e:
            print(f"[ERROR] Could not fetch data for {sym}: {e}")

# Asking User for Price Trend Graph
ask2=input("\nWould you like to get Today's Stock recommedation y\\n")
if(ask2=='y'):
    if __name__ == "__main__":
        DAYS=input("How Many days of price trend would you like to see ?")
        print("Starting to fetch and display 30-day stock price trends...\n")
        fetch_and_plot_stocks(official_symbol, DAYS)
        print("\nAll available stock graphs displayed successfully.")

