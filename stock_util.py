import os, sys
import string
class stock_util:
    def __init__(self):
        self.MARKET_SH = 1
        self.MARKET_SZ = 0
        self.MARKET_ELSE = 10

    '''
        def get_market(self, stock_code):
            if stock_code.startswith("SH"):
                return self.MARKET_SH
            elif stock_code.startswith("SZ"):
                return self.MARKET_SZ
            else:
                return self.MARKET_ELSE

        def get_market_name(self, stock_code):
            if stock_code.startswith("SH"):
                return "sh"
            elif stock_code.startswith("SZ"):
                return "sz"
            else:
                return "none"
    '''
    def get_market(self, stock_code):
        if (stock_code.startswith("6") or  stock_code.startswith("500") or  stock_code.startswith("550") or stock_code.startswith("510")) or stock_code.startswith("7"):
            return self.MARKET_SH
        elif (stock_code.startswith("00") or stock_code.startswith("30") or stock_code.startswith("150") or stock_code.startswith("159")):
            return self.MARKET_SZ
        else:
            return self.MARKET_ELSE

    def get_market_name(self, stock_code):
        if (stock_code.startswith("6") or  stock_code.startswith("500") or  stock_code.startswith("550") or stock_code.startswith("510")):
            return "sh"
        elif (stock_code.startswith("00") or stock_code.startswith("30") or stock_code.startswith("150") or stock_code.startswith("159")):
            return "sz"
        else:
            return "none"

    @classmethod
    def add_prifix(self, stock_code):
        if self.get_market_name(self, stock_code) == "sh":
            return "SH."+stock_code
        else:
            return "SZ."+stock_code



    def get_up_limit(self, price):
        return 0

    def get_down_limit(self, price):
        return 0
