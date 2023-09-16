import sys
import yfinance as yf
import csv
import time
import matplotlib.pyplot as plt
import datetime

# load current eur-usd exchange rate
tickerSymbol = 'EURUSD=X'
tickerData = yf.Ticker(tickerSymbol)
exchangeRate = tickerData.info['regularMarketOpen']

# assets in eur
EUROS = ['VWCE.DE', 'M44.BE', 'EUNM.DE', '82W.BE']


def save_to_file(value):
    with open("networth_over_time.csv", mode="a", newline="") as f:
        writer = csv.writer(f)

        # get current time
        current_time = int(time.time())

        # current_date_readable = datetime.datetime.fromtimestamp(current_time).date()

        # prepare data for csv
        data = [current_time, value]
        # write to csv
        writer.writerow(data)


def plot_networth():
    dates, values = read_from_csv()
    plt.plot(dates, values)

    plt.show()


def read_from_csv():
    values_array = []
    dates_array = []
    with open("networth_over_time.csv", mode="r") as f:
        reader = csv.reader(f)

        # skip header
        header = next(reader, None)

        for row in reader:
            unix_timestamp = int(row[0])
            date_object = datetime.datetime.fromtimestamp(unix_timestamp).date()
            values_array.append(float(row[1]))
            dates_array.append(date_object)

    return (dates_array, values_array)


def read_positions():
    tickers = []
    amounts = []
    with open("positions.csv", mode="r") as f:
        reader = csv.reader(f)

        # skip header
        header = next(reader, None)

        for row in reader:
            ticker = row[0]
            amount = float(row[1])

            # add to arrays
            tickers.append(ticker)
            amounts.append(amount)

    return tickers, amounts


def handle_cli() -> bool:
    """
    handles command line arguments and returns flag, whether networth should be plotted.

    possible flags:
        `-plot` - plots networth history.
        `-help` - show usage.

    :return: flag indicating, if networth should be plotted.
    """
    flag = False
    if len(sys.argv) >= 2:

        if sys.argv[1] == '-plot':
            flag = True

        else:
            sys.exit(1)

    return flag


def main():
    flag = handle_cli()

    # load positions from .csv
    tickers, amounts = read_positions()

    # calculate total value of all positions
    total_value = 0
    for i in range(len(tickers)):
        value = 0

        ticker = tickers[i]

        num_shares = amounts[i]

        value = yf.Ticker(ticker).info['regularMarketOpen'] * num_shares
        # special handling for euro assets:
        if ticker in EUROS:
            # calculate usd value of euro assets
            value = value * exchangeRate

        # print to terminal
        formatted_output = "ticker: {:<{width}} worth: {:{width}.2f}".format(ticker, value, width=15)
        print(formatted_output)

        total_value += value

    # convert to euro
    total_value /= exchangeRate
    total_value = round(total_value, 2)

    # print total value of portfolio
    print(f"Total portfolio value in €: {total_value:.2f}")

    # add to csv
    save_to_file(total_value)

    if flag:
        plot_networth()


if __name__ == '__main__':
    main()


