import requests
from requests.adapters import HTTPAdapter
import apikey
from asset import Asset

class PriceElement:
    def __init__(self):
        self.name = ""
        self.symbol = ""
        self.pid = 0
        self.price = 0

api_key = apikey.getapikey()

def fetch_trades():
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

def fetch_assets():
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

#function which uses bitpanda api v1. This function only returns prices for cryptocurrencies
def fetch_eur_prices():
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

def get_fiat_history():
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


def fetch_all_assets():
    CURRENCIES_URL = "https://api.bitpanda.com/v3/currencies"
    session = requests.Session()
    session.mount("https://", HTTPAdapter(max_retries=2))

    try:
        response = session.get(CURRENCIES_URL, timeout=10)
        response.raise_for_status()
        data = response.json()["data"]["attributes"]

        # Combine all asset categories into a single list
        all_assets = []
        for category in ["commodities", "cryptocoins", "leveraged_tokens",
                         "security_tokens", "index", "stocks", "etfs", "etcs"]:
            if category in data:
                all_assets.extend(data[category])

        return all_assets
    except requests.exceptions.RequestException as e:
        print(f"Error fetching assets: {e}")
        return None

def fetch_asset_price(asset_id):
    PRICES_URL = "https://api.bitpanda.com/v2/assets/prices?assetIds="
    try:
        response = requests.get(f"{PRICES_URL}{asset_id}", timeout=10)
        response.raise_for_status()
        price_data = response.json()["data"]
        if price_data:
            return price_data[0]["attributes"]["price"]
        return None
    except requests.exceptions.RequestException as e:
        print(f"Error fetching price for asset ID {asset_id}: {e}")
        return None

def get_price(assetlist):
    for asset in assetlist:
        asset.eur_value_single = fetch_asset_price(asset.id)

def fetch_asset_price(asset_id):
    PRICES_URL = "https://api.bitpanda.com/v2/assets/prices?assetIds="
    try:
        response = requests.get(f"{PRICES_URL}{asset_id}", timeout=10)
        response.raise_for_status()
        price_data = response.json()["data"]
        if price_data:
            return float(price_data[0]["attributes"]["price"])
        return None
    except requests.exceptions.RequestException as e:
        print(f"Error fetching price for asset ID {asset_id}: {e}")
        return None