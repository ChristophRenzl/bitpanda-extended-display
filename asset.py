from enum import Enum

class Assettype(Enum):
    none = 0
    commodities = 1
    cryptocoins = 2
    leveraged_tokens = 3
    security_tokens = 4
    index = 5
    stocks = 6
    etfs = 7
    etcs = 8

class Asset:
    def __init__(self):
        self.type = Assettype.none
        self.cryptocoin_symbol = ""
        self.balance = 0
        self.eur_value_single = 0
        self.value = 0
        self.id = 0
        self.pid = 0

    def __str__(self):
        return f"{self.cryptocoin_symbol}                       Value:{self.value}                   Number Owned:{self.balance}                 EurValSingle: {self.eur_value_single}"
