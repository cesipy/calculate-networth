
# Calculate Current Networth

This Python script calculates the current net worth of assets specified in a CSV file. The worth of assets is calculated in euros. Note that the currency calculation method may change in the future. The current net worth is saved to a file and can be plotted.

## Requirements

To run this script, you need to install `yfinance`, which can be done using:

```
pip install yfinance
```

You also need a file containing your positions/assets named `positions.csv`. The file should be structured as follows:

```
ticker,amount
BTC-USD,0.1
```

Historical net worth data is stored in `networth_over_time.csv`.

## Usage

To perform a simple calculation of the current net worth:

```bash
python src/main.py
```

To calculate the current net worth and plot the net worth history:

```bash
python src/main.py -plot
```

To only plot the net worth history:

```bash
python src/main.py -plotonly
```
