from domain.pmapi.pm_reader import PmReader
from domain.entities.position import Position
from domain.entities.report import Report
from datetime import date, timedelta
from infrastructure.util.util import json_str_to_date, generate_date_list, to_float
import json



def create_positions_from_json(json_str: str) -> list:
    po_list = json.loads(json_str)
    positions = []
    for po in po_list:
        position = Position(id=po.get("id"), open_date=json_str_to_date(po.get("open_date")),
                            open_price=to_float(po.get("open_price")), quantity=po.get("quantity"))
        position.close_date = json_str_to_date(po.get("close_date"))
        position.close_price = to_float(po.get("close_price"))
        if position.close_price:
            position.is_open = False
        position.transaction_costs = po.get("transaction_costs")
        position.instrument_id = po.get("instrument_id")
        position.instrument_currency = po.get("instrument_currency")
        position.open_transaction_type = po.get("open_transaction_type")
        positions.append(position)
    return positions

class PositionServices:

    def __init__(self, pm_reader: PmReader):
        self.pm_reader = pm_reader
        self.positions = None
        if not pm_reader:
            raise ValueError("PmReader cannot be null.")

    def load_from_json(self, json_str: str):
        self.positions = create_positions_from_json(json_str)

    def fill_positions(self, target_currency: str, start_date: date, end_date: date):
        for po in self.positions:
            po.start_date = start_date
            po.end_date = end_date
            # init dates
            po.init_dates()
            # read prices
            po.prices = self.pm_reader.read_instrument_prices(instrument_id=po.instrument_id, dates=po.dates)
            # read fx-rates
            if po.instrument_currency == target_currency:
                fx_rates = [1] * po.report_length
                po.target_rates = fx_rates
            else:
                pair = po.instrument_currency + target_currency
                fx_rates = self.pm_reader.read_fx_rates(pair=pair, dates=po.dates)
                po.target_rates = fx_rates
            # change the start to open price, if start is the open
            po.open_price_amend()
            # change the end to close price, if end is the close
            po.close_price_amend()
            # calculate values, target price and target values
            po.fill_values()
            # calculate is_open for each day
            po.set_is_opens()
            # calculate RPP and RPP%
            po.cal_returns()
        return self.positions

    def create_report(self, start_date: date, end_date: date):
        dates = generate_date_list(start_date=start_date, end_date=end_date)
        report = Report(dates=dates)
        report.fill_positions(self.positions)
        report.fill_baskets()
        return report


