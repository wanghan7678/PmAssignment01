from domain.pmapi.pm_reader import PmReader
from domain.entities.position import Position
from domain.entities.report import Report
from datetime import date, timedelta
from infrastructure.util.util import json_str_to_date, generate_date_list
import json


def generate_is_opens(position: Position) -> []:
    if position.is_open:
        is_open_value = 1
        start = position.open_date
        end = position.close_date if position.close_date else position.dates[-1]
        result = [0] * len(position.dates)
        dates = position.dates
        try:
            start_index = dates.index(start)
        except ValueError:
            start_index = 0 if start < dates[0] else len(dates)
        try:
            end_index = dates.index(end)
        except ValueError:
            end_index = len(dates) - 1 if end > dates[-1] else -1
        if start_index == len(dates) or end_index == -1:
            return result
        for i in range(start_index, end_index + 1):
            if i < len(dates):
                result[i] = is_open_value
        return result
    return [0] * len(position.dates)


def fill_empty(dates: [], values: [], value_start: date, value_end: date) -> []:
    if len(dates) == len(values):
        return values
    results = [0] * len(dates)
    start_index = dates.index(value_start)
    end_index = dates.index(value_end)
    for i in range(start_index, end_index + 1):
        if i < len(dates):
            results[i] = values[i - start_index]
    return results


def get_price_query(position: Position) -> []:
    query_start = position.dates[0]
    query_end = position.dates[-1]
    if position.open_date > position.dates[0]:
        query_start = position.open_date
    if position.close_date and position.close_date < position.dates[-1]:
        query_end = position.close_date
    return generate_date_list(start_date=query_start, end_date=query_end)


class PositionServices:

    def __init__(self, pm_reader: PmReader, positions: []):
        self.pm_reader = pm_reader
        self.positions = positions
        if not pm_reader:
            raise ValueError("PmReader cannot be null.")
        if not positions:
            raise ValueError("Position list cannot be empty.")

    def fill_positions(self, target_currency: str, start_date: date, end_date: date):
        for po in self.positions:
            if po.open_date > end_date or (po.close_date and po.close_date < start_date):
                raise ValueError("Report date out of the position scope.")
            dates = generate_date_list(start_date=start_date, end_date=end_date)
            po.dates = dates
            query_dates = get_price_query(po)
            prices = self.pm_reader.read_instrument_prices(instrument_id=po.instrument_id, dates=query_dates)
            if po.instrument_currency == target_currency:
                fx_rates = [1] * len(dates)
            else:
                pair = po.instrument_currency + target_currency
                fx_rates = self.pm_reader.read_fx_rates(pair=pair, dates=dates)
            po.prices = fill_empty(dates=po.dates, values=prices, value_start=query_dates[0], value_end=query_dates[-1])
            po.open_price_amend()
            po.close_price_amend()
            po.target_prices = [a * b for a, b in zip(po.prices, fx_rates)]
            po.is_opens = generate_is_opens(po)
        return self.positions

    def create_report(self, start_date: date, end_date: date):
        dates = generate_date_list(start_date=start_date, end_date=end_date)
        report = Report(dates=dates)
        report.fill_positions(self.positions)
        report.fill_baskets()
        return report

