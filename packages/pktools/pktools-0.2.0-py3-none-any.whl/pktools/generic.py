import toml
from time import sleep
import ccxt

# ────────────────────────────────────────────────────────────────────────────────


def simpleCountdown(seconds, message="Waiting..."):
    """Simple countdown with message

    Args:
        seconds (int): Duration of countdown in seconds
        message (str, optional): Message of countdown. Defaults to "Waiting...".
    """
    while seconds > 0:
        print(f" [{seconds}] {message}", end='\r')
        seconds -= 1
        sleep(1)

# ────────────────────────────────────────────────────────────────────────────────


def getPriceCryptoCurrency(pair, exchange="binance", price="last"):
    """Return price of a cryptocurrency

    Args:
        pair (str): Pair to use. Example: 'BTC/USDT'
        exchange (str, optional): Name of exchange. Defaults to "binance".
        price (str, optional): Price returned (last, bid or ask). Defaults to "last".

    Returns:
        float: Price returned
    """
    try:
        client = getattr(ccxt, exchange)()
        ticker = client.fetch_ticker(pair)
        return ticker[price]
    except Exception as e:
        print(e)
        return None

# ────────────────────────────────────────────────────────────────────────────────


def readTOML(filename):
    """Read TOML file and returns dictionary

    Args:
        filename (str): Filename path

    Returns:
        dict: Dictionary generated from file
    """
    try:
        with open(filename, 'r') as f:
            data = toml.load(f)
        return data
    except Exception as e:
        print(e)
    return None
