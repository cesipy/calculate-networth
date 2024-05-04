# Calculate Current Networth

This Python script calculates the current net worth of assets specified in a JSON file and a text file for euro assets. The worth of assets is calculated in euros. Note that the currency calculation method may change in the future. The current net worth is saved to a JSON file and can be plotted.

## Requirements
Before installing the dependencies, it is recommended to activate a virtual environment using `virtualenv` or `conda`. 
To run this script, you need to install the dependencies in your virtual environment:

```bash
pip install -r requirements.txt
```

You also need a file containing your positions/assets named `positions.json` and a text file named `positions_eur.txt` for euro assets (optional). The JSON file should be structured as follows:

```json
[
    {
        "ticker": "BTC-USD",
        "amount": 0.1,
        "avg_buy_price": "15000"
    },
    ...
]
```

The text file `positions_eur.txt` should contain euro asset values separated by commas:

```txt
1000,2000,3000
```

Historical net worth data is stored in `networth_over_time.json`. The file should be structured as follows:

```json
[
    {
        "time": "1000000000",
        "value": "1111",
        "investment_value": "1000"
    },
    ...
]
```

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