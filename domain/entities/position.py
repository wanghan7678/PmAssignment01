from datetime import date

DEFAULT_TARGET_CURRENCY = "USD"
TRANSACTION_TYPE_BUY = "BUY"
TRANSACTION_TYPE_SELL = "SELL"


class Position:

    def __init__(self, id, open_date: date, open_price, quantity):
        self.id = id
        self.is_open = True
        self.open_date = open_date
        self.close_date = None
        self.open_price = open_price
        self.close_price = None
        self.quantity = quantity
        self.transaction_costs = 0
        self.instrument_id = None
        self.instrument_currency = None
        self.open_transaction_type = TRANSACTION_TYPE_BUY
        self.dates = []
        self.prices = []
        self.is_opens = []
        self.target_currency = DEFAULT_TARGET_CURRENCY
        self.target_prices = []
        self.target_values = []


    def check_ready(self):
        return len(self.prices) == len(self.dates)

    def close_position(self, close_price, close_date):
        self.is_open = False,
        self.close_price = close_price
        self.close_date = close_date

    def open_price_amend(self):
        try:
            i = self.dates.index(self.open_date)
            self.prices[i] = self.open_price
        except ValueError:
            return

    def close_price_amend(self):
        if not self.close_price:
            return
        try:
            i = self.dates.index(self.close_date)
            self.prices[i] = self.close_price
        except ValueError:
            return

