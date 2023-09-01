import yfinance as yf
import csv
import time

# assets in eur
EUROS = ['VWCE.DE', 'M44.BE', 'EUNM.DE', '82W.BE']


def save_to_file(value):
    with open("networth_over_time.csv", mode="a", newline="") as f:
        writer = csv.writer(f)

        # get current time
        current_time = int(time.time())

        data = [current_time, value]

        writer.writerow(data)


# load current eur-usd exchange rate
tickerSymbol = 'EURUSD=X'
tickerData = yf.Ticker(tickerSymbol)
exchangeRate = tickerData.info['regularMarketOpen']

# load positions from file
with open("positions.txt") as f:
    positions = [line.strip().split(",") for line in f]

# calculate total value of all positions
total_value = 0
for i in positions:
    value = 0
    nested_arr = i[0].split()
    ticker = nested_arr[0]
    ticker = ticker[1:-1]
    num_shares = float(nested_arr[1])

    value = yf.Ticker(ticker).info['regularMarketOpen'] * num_shares
    # special handling:
    if ticker in EUROS:
        # print("reached!")
        value = value * exchangeRate

    formated_output = "ticker: {:<{width}} worth: {:{width}.2f}".format(ticker, value, width=15)
    print(formated_output)

    total_value += value

total_value /= exchangeRate
total_value = round(total_value, 2)

print(f"Total portfolio value in €: {total_value:.2f}")

# add to csv
save_to_file(total_value)
