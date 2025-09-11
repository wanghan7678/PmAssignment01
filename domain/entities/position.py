from datetime import date
from infrastructure.util.util import generate_date_list
from infrastructure.util.math_calculator import get_returns


DEFAULT_TARGET_CURRENCY = "USD"
TRANSACTION_TYPE_BUY = "BUY"
TRANSACTION_TYPE_SELL = "SELL"


class Position:

    def __init__(self, id, open_date: date, open_price, quantity):
        self.id = id
        self.is_open = True
        self.open_date = open_date
        self.close_date = None
        self.start_date = None
        self.end_date = None
        self.open_price = open_price
        self.open_day_price = None
        self.close_price = None
        self.close_day_price = None
        self.close_target_value = None
        self.quantity = quantity
        self.transaction_costs = 0
        self.instrument_id = None
        self.instrument_currency = None
        self.open_transaction_type = TRANSACTION_TYPE_BUY
        self.dates = []
        self.prices = []
        self.is_opens = []
        self.target_currency = DEFAULT_TARGET_CURRENCY
        self.target_rates = []
        self.target_prices = []
        self.target_values = []
        self.target_rpp = []
        self.target_rppp = []
        self.report_length = None

    def init_dates(self):
        if not self.start_date or not self.end_date or not self.open_date:
            raise ValueError(f"Position {self.id} with empty report start or end date.")
        if self.close_date and self.close_date < self.open_date:
            raise ValueError(f"Position {self.id}: out of the report date.")
        if self.open_date > self.end_date:
            raise ValueError(f"Position {self.id}: out of the report date.")
        if self.open_date > self.start_date:
            self.start_date = self.open_date
        if self.close_date and self.close_date < self.end_date:
            self.end_date = self.close_date
        self.dates = generate_date_list(start_date=self.start_date, end_date=self.end_date)
        self.report_length = len(self.dates)

    def fill_prices(self, prices):
        self.prices = prices
        self.open_price_amend()
        self.close_price_amend()

    def fill_values(self):
        if self.target_rates and len(self.target_rates) == self.report_length:
            self.target_prices = [x * r for x, r in zip(self.prices, self.target_rates)]
            self.target_values = [p * self.quantity for p in self.target_prices]
            if self.if_close_in_dates():
                self.close_target_value = self.target_values[-1]
                self.target_values[-1] = 0
        else:
            raise ValueError(f"Position {self.id}: target rates contains empty.")

    def set_is_opens(self):
        self.is_opens = [1] * self.report_length
        if self.if_close_in_dates():
            self.is_opens[-1] = 0


    def cal_returns(self):
        open_day_value = self.open_day_price * self.quantity if self.open_day_price else None
        values = [x for x in self.target_values]
        if self.if_close_in_dates():
            values[-1] = self.close_target_value
        R, RP = get_returns(value_list=values, open_type=self.open_transaction_type,
                           open_day_value=open_day_value)
        if self.if_open_in_dates():
            open_day_target_value = open_day_value * self.target_rates[0]
            R[1] = (self.target_values[1] - open_day_target_value)
            RP[1] = R[1] / open_day_target_value
        self.target_rpp = R
        self. target_rppp = RP


    def check_ready(self):
        return len(self.prices) == len(self.dates)

    def close_position(self, close_price, close_date):
        self.is_open = False,
        self.close_price = close_price
        self.close_date = close_date

    def close_price_amend(self):
        if self.close_date and self.close_date == self.end_date:
            self.close_day_price = self.prices[-1]
            self.prices[-1] = self.close_price

    def open_price_amend(self):
        if self.start_date == self.open_date:
            self.open_day_price = self.prices[0]
            self.prices[0] = self.open_price

    def if_open_in_dates(self):
        return self.open_date == self.start_date

    def if_close_in_dates(self):
        return self.close_date and self.close_date == self.end_date