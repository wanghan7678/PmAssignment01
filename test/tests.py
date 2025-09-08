import unittest
from infrastructure.util.util import generate_date_list, json_str_to_date, to_float
from domain.entities.position import Position
from infrastructure.pmapi.pm_reader_impl import PmReaderImpl
import json

START_DATE = "2023-01-01"
END_DATE = "2024-11-10"
json_file = "/Users/hanwang/downloads/tech-challenge-2025-positions.json"
json_str = '[{"id":299825,"open_date":"2022-11-01","close_date":"2024-10-20","open_price":"90.515","close_price":"160","quantity":35,"transaction_costs":0,"instrument_id":10256,"instrument_currency":"USD","open_transaction_type":"BUY","close_transaction_type":"SELL"},{"id":299826,"open_date":"2023-01-10","close_date":null,"open_price":"80","close_price":null,"quantity":50,"transaction_costs":0,"instrument_id":10256,"instrument_currency":"USD","open_transaction_type":"BUY","close_transaction_type":null},{"id":299827,"open_date":"2023-05-11","close_date":null,"open_price":"116","close_price":null,"quantity":35,"transaction_costs":0,"instrument_id":10256,"instrument_currency":"USD","open_transaction_type":"BUY","close_transaction_type":null},{"id":299828,"open_date":"2022-11-01","close_date":null,"open_price":"90.515","close_price":null,"quantity":65,"transaction_costs":0,"instrument_id":10256,"instrument_currency":"USD","open_transaction_type":"BUY","close_transaction_type":null},{"id":299832,"open_date":"2023-02-06","close_date":"2024-09-12","open_price":"115","close_price":"125","quantity":23,"transaction_costs":0,"instrument_id":32,"instrument_currency":"EUR","open_transaction_type":"BUY","close_transaction_type":"SELL"},{"id":299833,"open_date":"2023-07-03","close_date":null,"open_price":"133","close_price":null,"quantity":50,"transaction_costs":0,"instrument_id":32,"instrument_currency":"EUR","open_transaction_type":"BUY","close_transaction_type":null},{"id":299834,"open_date":"2023-02-06","close_date":null,"open_price":"115","close_price":null,"quantity":50,"transaction_costs":0,"instrument_id":32,"instrument_currency":"EUR","open_transaction_type":"BUY","close_transaction_type":null},{"id":299841,"open_date":"2023-04-12","close_date":"2024-07-10","open_price":"1527","close_price":"1635.5","quantity":129,"transaction_costs":0,"instrument_id":21289,"instrument_currency":"SEK","open_transaction_type":"BUY","close_transaction_type":"SELL"},{"id":299842,"open_date":"2024-02-12","close_date":"2024-08-26","open_price":"1275","close_price":"1763","quantity":101,"transaction_costs":0,"instrument_id":21289,"instrument_currency":"SEK","open_transaction_type":"BUY","close_transaction_type":"SELL"},{"id":299843,"open_date":"2023-04-12","close_date":"2024-08-26","open_price":"1527","close_price":"1763","quantity":71,"transaction_costs":0,"instrument_id":21289,"instrument_currency":"SEK","open_transaction_type":"BUY","close_transaction_type":"SELL"},{"id":299844,"open_date":"2024-02-12","close_date":null,"open_price":"1275","close_price":null,"quantity":36,"transaction_costs":0,"instrument_id":21289,"instrument_currency":"SEK","open_transaction_type":"BUY","close_transaction_type":null},{"id":299845,"open_date":"2023-05-19","close_date":null,"open_price":"0.2192","close_price":null,"quantity":1823,"transaction_costs":0,"instrument_id":21290,"instrument_currency":"DKK","open_transaction_type":"BUY","close_transaction_type":null}]'


def test_json(json_str: str) -> []:
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


if __name__ == "__main__":
    start = json_str_to_date("2022-11-01")
    end = json_str_to_date("2024-10-20")
    dates = generate_date_list(start_date=start, end_date=end)
    pm_reader = PmReaderImpl()
    r = pm_reader.read_fx_rates(pair="EURUSD", dates=dates)
    print(r)
