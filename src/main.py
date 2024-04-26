import sys
import yfinance as yf
import csv
import time
import matplotlib.pyplot as plt
import datetime
import typing
from logger import Logger
import argparse

POSITIONS_FILE_PATH = "res/positions.csv"
NETWORTH_FILE_PATH = "res/networth_over_time.csv"

# assets in euro
EUROS = ['VWCE.DE', 'M44.BE', 'EUNM.DE', '82W.BE', 'Bank_Sparbuch', 'Bank_N26', 'Bank_Raika']  # insert here!

# load current eur-usd exchange rate
tickerSymbol = 'EURUSD=X'
tickerData = yf.Ticker(tickerSymbol)
exchangeRate = tickerData.info['regularMarketOpen']

logger = Logger()

def calculate_value(ticker: str, num_shares: float) -> float:
    if ticker.startswith("Bank") or ticker.startswith("bank"):
        return num_shares
    return yf.Ticker(ticker).info['regularMarketOpen'] * num_shares


def write_networth_to_file(value: float):
    """
    saves current networth `value`.
    """
    with open(NETWORTH_FILE_PATH, mode="a", newline="") as f:
        writer = csv.writer(f)

        current_time = int(time.time())

        # prepare data for csv
        data = [current_time, value]
        # write to csv
        writer.writerow(data)


def plot_networth_history():
    """
    plots networth history in a coordinate system using time in x axis and value on y axis.
    """
    dates, values = load_networth_history()

    plt.figure(figsize=(10, 6))
    
    plt.plot(dates, values)
    plt.xlabel("Date")
    plt.ylabel("Networth in €")

    plt.show()


def load_networth_history() -> typing.Tuple[typing.List[int], typing.List[int]]:
    """
    reads historical data from .csv.
    """
    values_array = []
    dates_array = []
    with open(NETWORTH_FILE_PATH, mode="r") as f:
        reader = csv.reader(f)

        # skip header
        header = next(reader, None)

        for row in reader:
            unix_timestamp = int(row[0])
            date_object = datetime.datetime.fromtimestamp(unix_timestamp).date()
            values_array.append(float(row[1]))
            dates_array.append(date_object)

    return (dates_array, values_array)


def load_positions() -> typing.Tuple[typing.List[str], typing.List[int]]:
    """
    reads positions from .csv.
    """
    tickers = []
    amounts = []
    with open(POSITIONS_FILE_PATH, mode="r") as f:
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
        `--plot` - plots networth history.
        `--help` - show usage.

    :return: flag indicating, if networth should be plotted.
    """
    parser = argparse.ArgumentParser(description='Calculate and plot net worth.')
    parser.add_argument('--plot', action='store_true', help='Plot networth history.')
    parser.add_argument('--plotonly', action='store_true', help='Only plot networth history, do not calculate current networth.')
    
    args = parser.parse_args()

    if args.plotonly:
        plot_networth_history()
        sys.exit(1)     # exit early, don't want to calculate current networth

    return args.plot


def main():
    flag = handle_cli()

    # load positions from .csv
    tickers, amounts = load_positions()

    # calculate total value of all positions
    total_value = 0
    for i in range(len(tickers)):
        value = 0

        ticker = tickers[i]

        num_shares = amounts[i]

        #value = yf.Ticker(ticker).info['regularMarketOpen'] * num_shares+
        value = calculate_value(ticker, num_shares)
        # special handling for euro assets:
        if ticker in EUROS:
            # calculate usd value of euro assets
            value = value * exchangeRate

        formatted_output = "ticker: {:<{width}} worth: {:{width}.2f}".format(ticker, value, width=15)
        logger.log(formatted_output)
        print(formatted_output)

        total_value += value

    # convert to euro
    total_value /= exchangeRate
    total_value = round(total_value, 2)

    logger.log(f"Total portfolio value in €: {total_value:.2f}")
    print(f"Total portfolio value in €: {total_value:.2f}")

    # add to csv
    write_networth_to_file(total_value)

    if flag:
        plot_networth_history()


if __name__ == '__main__':
    main()


