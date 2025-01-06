import requests
import apikey
from urllib.parse import urljoin

class Asset:
    def __init__(self):
        self.cryptocoin_symbol = ""
        self.balance = 0
        self.eur_value_single = 0
        self.value = 0

    def __str__(self):
        return f"{self.cryptocoin_symbol}                       Value:{self.value}                   Number Owned:{self.balance}                 EurValSingle: {self.eur_value_single}"

def fetch_trades(api_key):
    """Fetch trade data from the Bitpanda API and display a summary."""
    url = "https://api.bitpanda.com/v1/trades"
    try:
        headers = {"X-Api-Key": api_key}
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        trades_data = response.json()
        trades_data1 = response.json()
        return trades_data1
        #display_trade_summary(trades_data)
    except requests.exceptions.RequestException as e:
        print(f"Error fetching trades data: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        #return trades_data1

def fetch_assets(api_key):
    """Fetch asset data from the Bitpanda API and display a summary."""
    url = "https://api.bitpanda.com/v1/asset-wallets"
    try:
        headers = {"X-Api-Key": api_key}
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        assets_data = response.json()
        #display_asset_summary(assets_data, api_key)
    except requests.exceptions.RequestException as e:
        print(f"Error fetching assets data: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    return assets_data

def fetch_eur_prices(api_key):
    """Fetch the EUR prices for assets from Bitpanda."""
    url = "https://api.bitpanda.com/v1/ticker"
    try:
        headers = {"X-Api-Key": api_key}
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        ticker_data = response.json()
        return {symbol: data['EUR'] for symbol, data in ticker_data.items()}
    except requests.exceptions.RequestException as e:
        print(f"Error fetching EUR prices: {e}")
        return {}
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return {}

def display_trade_summary(trades_data):
    """Display the total fiat spent and differences for all trades."""
    if not trades_data or "data" not in trades_data:
        print("No trade data available.")
        return

    trade_summary = {}

    for trade in trades_data["data"]:
        attributes = trade["attributes"]
        trade_type = attributes["type"]
        fiat_amount = float(attributes["amount_fiat"])

        if trade_type not in trade_summary:
            trade_summary[trade_type] = 0

        trade_summary[trade_type] += fiat_amount

    print("Trade Summary:")
    for trade_type, total_fiat in trade_summary.items():
        print(f"- {trade_type}: {total_fiat:.2f} EUR")

def display_asset_summary(assets_data, api_key):
    """Display the owned assets and their performance."""
    if not assets_data or "data" not in assets_data:
        print("No asset data available.")
        return
    else:
        assets_data = assets_data["data"]
        #list attributes
        assets_data = assets_data["attributes"]
        assets_cryptocoin = assets_data["cryptocoin"]
        assets_commodity = assets_data["commodity"]
        assets_index = assets_data["index"]
        assets_security = assets_data["security"]
        assets_stock = assets_security["stock"]
        assets_etf = assets_security["etf"]
        assets_fiat_earn = assets_security["fiat_earn"]


#printfunction
def print_asset(asset, eur_dict):
    for data in asset["attributes"]["wallets"]:
        print(f"- {data['attributes']['cryptocoin_symbol']}: {data['attributes']['balance']:}")

#crypto
def get_crypto_wallets(api_key):
    assets = fetch_assets(api_key)
    return assets["data"]["attributes"]["cryptocoin"]

def print_crypto_wallets(cryptowallets):
    print_asset(cryptowallets)
    return

def add_cryptos(cryptowallets, eur_dict, list):
    for asset in cryptowallets["attributes"]["wallets"]:
        tmp = Asset()
        tmp.cryptocoin_symbol = asset["attributes"]["cryptocoin_symbol"]
        tmp.balance = float(asset["attributes"]["balance"])
        #find tmp.cryptocoin_symbol in eur_dict
        if tmp.cryptocoin_symbol in eur_dict:
            tmp.eur_value_single = float(eur_dict[tmp.cryptocoin_symbol])
        #calculate actual value
        tmp.value = tmp.eur_value_single * tmp.balance
        list.append(tmp)


#commodity
def get_commodity(api_key):
    assets = fetch_assets(api_key)
    return assets["data"]["attributes"]["commodity"]["metal"]

def print_commodity(commodity):
    print('commodity:')
    for data in commodity["metal"]["attributes"]["wallets"]:
        print(f"- {data['attributes']["cryptocoin_symbol"]}: {data['attributes']['balance']:}")
    return

def add_commodity(data, eur_dict, list):
    for asset in data["attributes"]["wallets"]:
        tmp = Asset()
        tmp.cryptocoin_symbol = asset["attributes"]["cryptocoin_symbol"]
        tmp.balance = float(asset["attributes"]["balance"])
        #find tmp.cryptocoin_symbol in eur_dict
        if tmp.cryptocoin_symbol in eur_dict:
            tmp.eur_value_single = float(eur_dict[tmp.cryptocoin_symbol])
        #calculate actual value
        tmp.value = tmp.eur_value_single * tmp.balance
        list.append(tmp)

#stock
def get_stock(api_key):
    assets = fetch_assets(api_key)
    return assets["data"]["attributes"]["security"]["stock"]

def add_asset(data, eur_dict, list):
    for asset in data["attributes"]["wallets"]:
        tmp = Asset()
        tmp.cryptocoin_symbol = asset["attributes"]["cryptocoin_symbol"]
        tmp.balance = float(asset["attributes"]["balance"])
        #find tmp.cryptocoin_symbol in eur_dict
        if tmp.cryptocoin_symbol in eur_dict:
            tmp.eur_value_single = float(eur_dict[tmp.cryptocoin_symbol])
        #calculate actual value
        tmp.value = tmp.eur_value_single * tmp.balance
        list.append(tmp)

#etf
def get_etf(api_key):
    assets = fetch_assets(api_key)
    return assets["data"]["attributes"]["security"]["etf"]

#etc
def get_etc(api_key):
    assets = fetch_assets(api_key)
    return assets["data"]["attributes"]["security"]["etc"]

#fiat_earn
def get_fiat(api_key):
    assets = fetch_assets(api_key)
    return assets["data"]["attributes"]["security"]["fiat_earn"]


def get_fiat_history(api_key):
    """Fetch all fiat transaction history data using cursor-based pagination from the Bitpanda API."""
    base_url = "https://api.bitpanda.com/v1/fiatwallets/transactions"
    fiat_data = []
    next_cursor = None  # Initialize cursor as None

    while True:
        try:
            headers = {"X-Api-Key": api_key}
            params = {"cursor": next_cursor} if next_cursor else {}
            response = requests.get(base_url, headers=headers, params=params)
            response.raise_for_status()
            data = response.json()

            # Filter and append only items with type 'deposit'
            deposit_data = [
                item for item in data.get("data", [])
                if item.get("attributes", {}).get("type") == "deposit" and item.get("attributes", {}).get("status") != "canceled"
            ]
            fiat_data.extend(deposit_data)

            # Access next_cursor from the nested meta dictionary
            next_cursor = data.get("meta", {}).get("next_cursor")
            if not next_cursor:  # Stop if there's no next cursor
                break
        except requests.exceptions.RequestException as e:
            print(f"Error fetching fiat data: {e}")
            break  # Exit loop on error

    return fiat_data

def get_money_spent(api_key):
    list_trades = get_fiat_history(api_key)
    sum = 0
    for element in list_trades:
        sum += float(element.get("attributes", {}).get("amount", 0))
    return sum

if __name__ == "__main__":
    api_key = apikey.getapikey()

    money_spent = get_money_spent(api_key)

    eur_dict_cryptos = fetch_eur_prices(api_key)
    EURVALUE = 0
    all_assets = []

    #cryptos
    list_cryptos = []
    print("cryptos:")
    cryptos = get_crypto_wallets(api_key)
    add_asset(cryptos, eur_dict_cryptos, list_cryptos)
    add_asset(cryptos, eur_dict_cryptos, all_assets)
    for element in list_cryptos:
        print(element)

    #commodity
    list_commodity = []
    print("commodity:")
    commodity = get_commodity(api_key)
    add_asset(commodity, eur_dict_cryptos, list_commodity)
    add_asset(commodity, eur_dict_cryptos, all_assets)
    for element in list_commodity:
        print(element)


    #stock
    list_stock = []
    print("stock:")
    stock = get_stock(api_key)
    add_asset(stock, eur_dict_cryptos, list_stock)
    add_asset(stock, eur_dict_cryptos, all_assets)
    for element in list_stock:
        print(element)


    #etf
    list_etf = []
    print("etf:")
    etf = get_etf(api_key)
    add_asset(etf, eur_dict_cryptos, list_etf)
    add_asset(etf, eur_dict_cryptos, all_assets)
    for element in list_etf:
        print(element)


    #etc
    list_etc = []
    print("etc:")
    etc = get_etc(api_key)
    add_asset(etc, eur_dict_cryptos, list_etc)
    add_asset(etc, eur_dict_cryptos, all_assets)
    for element in list_etc:
        print(element)


    #fiat
    list_fiat = []
    print("fiat:")
    fiat = get_fiat(api_key)
    add_asset(fiat, eur_dict_cryptos, list_fiat)
    add_asset(fiat, eur_dict_cryptos, all_assets)
    for element in list_fiat:
        print(element)


    print("crypto value:")
    tmp = 0
    for element in list_cryptos:
        tmp += element.value
    print(tmp)

    tmp = 0
    print("gold...:")
    for element in list_commodity:
        tmp += element.value
    print(tmp)

    tmp = 0
    print("stocks")
    for element in list_stock:
        tmp += element.value
    print(tmp)

    tmp = 0
    print("etfs")
    for element in list_etf:
        tmp += element.value
    print(tmp)

    print("Overall value:")
    for element in all_assets:
        EURVALUE += element.value
    print(EURVALUE)

    #print all spent value
    print("Spent value:")
    print(money_spent)