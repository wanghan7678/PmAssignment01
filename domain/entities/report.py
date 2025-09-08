from domain.entities.position import Position
from infrastructure.util.math_calculator import get_return_list, get_round
import json

NAME_IS_OPEN = "IsOpen"
NAME_PRICE = "Price"
NAME_VALUE = "Value"
NAME_RPP = "ReturnPerPeriod"
NAME_RPPP = "ReturnPerPeriodPercentage"
NAME_DATE = "dates"


class Report:

    def __init__(self, dates: list):
        self.positions = dict()
        self.basket = dict()
        self.dates = dates
        if not self.dates:
            raise ValueError("The report dates are empty.")
        self.dates.sort()
        self.length = len(self.dates)
        self.basket[NAME_IS_OPEN] = [0] * self.length
        self.basket[NAME_PRICE] = [0] * self.length
        self.basket[NAME_VALUE] = [0] * self.length
        self.basket[NAME_RPP] = [0] * self.length
        self.basket[NAME_RPPP] = [0] * self.length

    def __len__(self):
        return self.length

    def fill_positions(self, positions: list):
        for po in positions:
            if not isinstance(po, Position):
                raise ValueError("The input position is not a Position type.")
            if not self.check_position_ready(po):
                raise ValueError("Position data not ready.")
            self.positions[po.id] = {
                NAME_IS_OPEN: [],
                NAME_PRICE: [],
                NAME_VALUE: [],
                NAME_RPP: [],
                NAME_RPPP: []
            }
            self.positions[po.id][NAME_IS_OPEN] = po.is_opens
            self.positions[po.id][NAME_PRICE] = [get_round(i) for i in po.prices]
            self.positions[po.id][NAME_PRICE] = [get_round(i) for i in po.target_prices]
            self.positions[po.id][NAME_VALUE] = [get_round(s * po.quantity) for s in po.target_prices]
            R, RP = get_return_list(value_list=self.positions[po.id][NAME_VALUE], open_type=po.open_transaction_type,
                                    close_index=po.get_close_index())
            self.positions[po.id][NAME_RPP] = [get_round(i) for i in R]
            self.positions[po.id][NAME_RPPP] = [get_round(i) for i in RP]

    def check_position_ready(self, position: Position):
        return len(position.dates) == len(self.dates)

    # there are two method to calculate the
    def fill_baskets(self):
        prices = []
        is_opens = []
        values = []
        rpp = []
        rppp = []
        for k, v in self.positions.items():
            is_opens.append(v[NAME_IS_OPEN])
            prices.append(v[NAME_PRICE])
            values.append(v[NAME_VALUE])
            rpp.append(v[NAME_RPP])
            rppp.append(v[NAME_RPPP])
        self.basket[NAME_IS_OPEN] = [get_round(sum(c)) for c in zip(*is_opens)]
        self.basket[NAME_PRICE] = [get_round(sum(c)) for c in zip(*prices)]
        self.basket[NAME_VALUE] = [get_round(sum(c))for c in zip(*values)]
        self.basket[NAME_IS_OPEN] = [1 if x >= 1 else x for x in self.basket[NAME_IS_OPEN]]
        # self.basket[NAME_RPP] = [sum(c) for c in zip(*rpp)]
        # self.basket[NAME_RPPP] = [sum(c) for c in zip(*rppp)]
        R, RP = get_return_list(value_list=self.basket[NAME_VALUE])
        self.basket[NAME_RPP] = [get_round(i) for i in R]
        self.basket[NAME_RPPP] = [get_round(i) for i in RP]


