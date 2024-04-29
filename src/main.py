import sys
import yfinance as yf
import csv
import time
import matplotlib.pyplot as plt
import datetime
import typing
from logger import Logger
import argparse
import json
import os

POSITIONS_FILE_PATH = "res/positions.json"
NETWORTH_FILE_PATH  = "res/networth_over_time.json"
EUROS_PATH          = "res/positions_eur.txt"


def get_euro_assets(path: str): 
    # if file does not exists, just return empty list
    if not os.path.exists(path):
        return []
    with open(path, "r") as f:
        data = f.read()
    
    euros = data.split(",")

    return euros


# assets in euro
EUROS = get_euro_assets(EUROS_PATH)  # insert here!

# load current eur-usd exchange rate
tickerSymbol = 'EURUSD=X'
tickerData = yf.Ticker(tickerSymbol)
exchangeRate = tickerData.info['regularMarketOpen']

logger = Logger()




def calculate_value(ticker: str, num_shares: float) -> float:
    if ticker.startswith("Bank") or ticker.startswith("bank"):
        return num_shares
    return yf.Ticker(ticker).info['regularMarketOpen'] * num_shares


def write_networth_to_file(current_value: float, invested_money: float ):
    """
    saves current networth `value`.
    """
    current_time = int(time.time())
    new_data     = {'time': str(current_time), 'value': str(current_value), 'investment_value':str(invested_money)}

       # Read existing data
    try:
        with open(NETWORTH_FILE_PATH, "r") as f:
            data = json.load(f)
    except FileNotFoundError:
        data = []

    data.append(new_data)

    with open(NETWORTH_FILE_PATH, "w") as f:
        json.dump(data, f, indent=4)


def plot_networth_history():
    """
    plots networth history in a coordinate system using time in x axis and value on y axis.
    """
    dates, values, investment_values = load_networth_history()

    plt.figure(figsize=(10, 6))
    
    plt.plot(dates, values, label='Net Worth')
    plt.plot(dates, investment_values, color='green', label='Investment Value')
    plt.xlabel("Date")
    plt.ylabel("Value in €")
    plt.legend()

    plt.show()


def load_networth_history() -> typing.Tuple[typing.List[int], typing.List[int]]:
    """
    reads historical data from .csv.
    """
    values_array = []
    dates_array = []
    investment_values = []
    with open(NETWORTH_FILE_PATH, mode="r") as f:
        data_list = json.load(f)
    
    for data in data_list:
        unix_timestamp = int(data['time'])
        formatted_date = datetime.datetime.fromtimestamp(unix_timestamp).date()
        value          = float(data['value'])
        investment_value = float(data['investment_value'])

        values_array.append(value)
        dates_array.append(formatted_date)
        investment_values.append(investment_value)

    return (dates_array, values_array, investment_values)


def load_positions() -> typing.Tuple[typing.List[str], typing.List[int]]:
    """
    reads positions from .csv.
    """
    tickers = []
    amounts = []
    avg_prices = []
    
    with open(POSITIONS_FILE_PATH, "r") as f: 
        data_list = json.load(f)

    for data in data_list:
        tickers.append(data['ticker'])
        amounts.append(float(data['amount']))
        avg_prices.append(float(data['avg_buy_price']))

    return tickers, amounts, avg_prices


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
    tickers, amounts, avg_prices = load_positions()

    # calculate total value of all positions
    total_current_value = 0
    total_buy_value     = 0
    for i in range(len(tickers)):
        value = 0
        buy_amount = 0

        ticker = tickers[i]
        num_shares = amounts[i]
        avg_price  = avg_prices[i]

        value = calculate_value(ticker, num_shares)

        if ticker.startswith("Bank"):
            buy_amount = num_shares
        else: 
            buy_amount = num_shares * avg_price

        # special handling for euro assets:
        if ticker in EUROS:
            # calculate usd value of euro assets
            value = value * exchangeRate
            buy_amount = buy_amount * exchangeRate

        formatted_output = "ticker: {:<{width}} worth: {:{width}.2f}".format(ticker, value, width=15)
        logger.log(formatted_output)
        print(formatted_output)

        total_current_value += value
        total_buy_value += buy_amount

    # convert to euro
    total_current_value /= exchangeRate
    total_current_value = round(total_current_value, 2)

    total_buy_value /= exchangeRate
    total_buy_value = round(total_buy_value, 2)

    logger.log(f"Total portfolio value in €: {total_current_value:.2f}")
    print(f"Total portfolio value in €: {total_current_value:.2f}")
    print(f"Invested value in €: {total_buy_value:.2f}")

    # add to csv
    write_networth_to_file(total_current_value, invested_money=total_buy_value)

    if flag:
        plot_networth_history()


if __name__ == '__main__':
    main()


