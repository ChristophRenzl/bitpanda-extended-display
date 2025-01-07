import apiFunctions
from asset import Asset, Assettype

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


def print_asset(asset, eur_dict):
    for data in asset["attributes"]["wallets"]:
        print(f"- {data['attributes']['cryptocoin_symbol']}: {data['attributes']['balance']:}")

#crypto
def get_crypto_wallets():
    assets = apiFunctions.fetch_assets()
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
def get_commodity():
    assets = apiFunctions.fetch_assets()
    return assets["data"]["attributes"]["commodity"]["metal"]

def print_commodity(commodity):
    print('commodity:')
    for data in commodity["metal"]["attributes"]["wallets"]:
        print(f"- {data['attributes']["cryptocoin_symbol"]}: {data['attributes']['balance']:}")
    return

def add_commodity(data, list):
    for asset in data["attributes"]["wallets"]:
        tmp = Asset()
        tmp.cryptocoin_symbol = asset["attributes"]["cryptocoin_symbol"]
        tmp.id = asset["attributes"]["cryptocoin_id"]
        tmp.balance = float(asset["attributes"]["balance"])
        #find tmp.cryptocoin_symbol in eur_dict
        # if tmp.cryptocoin_symbol in eur_dict:
        #     tmp.eur_value_single = float(eur_dict[tmp.cryptocoin_symbol])
        #calculate actual value
        # tmp.value = tmp.eur_value_single * tmp.balance
        list.append(tmp)

#stock
def get_stock():
    assets = apiFunctions.fetch_assets()
    return assets["data"]["attributes"]["security"]["stock"]

def add_asset(data, list):
    for asset in data["attributes"]["wallets"]:
        tmp = Asset()
        tmp.cryptocoin_symbol = asset["attributes"]["cryptocoin_symbol"]
        tmp.balance = float(asset["attributes"]["balance"])
        tmp.id = asset["attributes"]["cryptocoin_id"]
        #find tmp.cryptocoin_symbol in eur_dict
        # if tmp.cryptocoin_symbol in eur_dict:
        #     tmp.eur_value_single = float(eur_dict[tmp.cryptocoin_symbol])
        # #calculate actual value
        # tmp.value = tmp.eur_value_single * tmp.balance
        list.append(tmp)

#etf
def get_etf():
    assets = apiFunctions.fetch_assets()
    return assets["data"]["attributes"]["security"]["etf"]

#etc
def get_etc():
    assets = apiFunctions.fetch_assets()
    return assets["data"]["attributes"]["security"]["etc"]

#fiat_earn
def get_fiat():
    assets = apiFunctions.fetch_assets()
    return assets["data"]["attributes"]["security"]["fiat_earn"]


def get_money_spent():
    list_trades = apiFunctions.get_fiat_history()
    sum = 0
    for element in list_trades:
        sum += float(element.get("attributes", {}).get("amount", 0))
    return sum

def get_All_Assets():
    tmp = []
    cryptos = get_crypto_wallets()
    add_asset(cryptos, tmp)
    commodity = get_commodity()
    add_commodity(commodity, tmp)
    stock = get_stock()
    add_asset(stock, tmp)
    etf = get_etf()
    add_asset(etf, tmp)
    etc = get_etc()
    add_asset(etc, tmp)
    fiat = get_fiat()
    add_asset(fiat, tmp)

    #getPrices
    apiFunctions.get_price(tmp)

    #calculate value
    for asset in tmp:
        if asset.balance == None or asset.eur_value_single == None:
            asset.value = 0
        else:
            asset.value = float(asset.balance * asset.eur_value_single)

    return tmp

if __name__ == "__main__":
    all_assets = []
    AssetValueEUR = 0
    money_spent = get_money_spent()
    all_assets = get_All_Assets()

    for asset in all_assets:
        print(asset)

    for asset in all_assets:
        AssetValueEUR += float(asset.value)

    print("Overall value (without staked, without assets singleEurVal >0,001):")
    print(AssetValueEUR)

    #print all spent value
    print("Spent value:")
    print(money_spent)