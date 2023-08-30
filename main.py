import yfinance as yf

GERMANS = ['VWCE.DE','M44.BE', 'EUNM.DE', '82W.BE']

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
    if ticker in GERMANS:
        #print("reached!")
        value = value * exchangeRate

    formated_output = "ticker: {:<{width}} worth: {:{width}.2f}".format(ticker, value, width=15)
    print(formated_output)

    total_value += value

total_value/= exchangeRate
print(f"Total portfolio value in €: {total_value:.2f}")
