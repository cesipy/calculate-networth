
# Calculate Current Networth

This Python script calculates the current net worth of assets specified in a CSV file. 
The worth of assets is calculated in euros. Note that the currency calculation method may change in the future. The current net worth is saved to a file and can be plotted.

## Requirements
To run this script, you need to install `yfinance`, which can be done using:
```
pip install yfinance
```

You also need a file containing your positions/assets named `positions.csv`. 
The file should be structured as follows:
```
ticker,amount
BTC-USD,0.1
```

Historical net worth data is stored in `networth_over_time.csv`. The file should be structured as follows:
```
time, value
1692343236,1111
```
In order to do this copy `positions.csv.sample` to `positions.csv`. Do the same for 
`networth_over_time.csv.sample`

## Usage
To perform a simple calculation of the current net worth:

```bash
python main.py
```

To calculate the current net worth and plot the net worth history:

```bash
python main.py -plot
```

To only plot the net worth history:

```bash
python main.py -plotonly
```
