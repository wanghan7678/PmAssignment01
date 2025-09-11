import datetime
from django.test import TestCase
from datetime import date

from domain.entities.position import Position
from domain.services.position_services import create_positions_from_json


def create_position(id, open_date, close_date, start_date, end_date,
                    open_price, close_price, quantity):
    po = Position(id=id, open_date=open_date,
                  open_price=open_price, quantity=quantity)
    po.close_price = close_price
    po.instrument_currency = "USD"
    po.target_currency = "USD"
    po.close_date = close_date
    po.start_date = start_date
    po.end_date = end_date
    po.init_dates()
    return po


class PositionTestCase(TestCase):
    # json_str = '[{"id":299825,"open_date":"2022-11-01","close_date":"2024-10-20","open_price":"90.515","close_price":"160","quantity":35,"transaction_costs":0,"instrument_id":10256,"instrument_currency":"USD","open_transaction_type":"BUY","close_transaction_type":"SELL"},{"id":299826,"open_date":"2023-01-10","close_date":null,"open_price":"80","close_price":null,"quantity":50,"transaction_costs":0,"instrument_id":10256,"instrument_currency":"USD","open_transaction_type":"BUY","close_transaction_type":null},{"id":299827,"open_date":"2023-05-11","close_date":null,"open_price":"116","close_price":null,"quantity":35,"transaction_costs":0,"instrument_id":10256,"instrument_currency":"USD","open_transaction_type":"BUY","close_transaction_type":null},{"id":299828,"open_date":"2022-11-01","close_date":null,"open_price":"90.515","close_price":null,"quantity":65,"transaction_costs":0,"instrument_id":10256,"instrument_currency":"USD","open_transaction_type":"BUY","close_transaction_type":null},{"id":299832,"open_date":"2023-02-06","close_date":"2024-09-12","open_price":"115","close_price":"125","quantity":23,"transaction_costs":0,"instrument_id":32,"instrument_currency":"EUR","open_transaction_type":"BUY","close_transaction_type":"SELL"},{"id":299833,"open_date":"2023-07-03","close_date":null,"open_price":"133","close_price":null,"quantity":50,"transaction_costs":0,"instrument_id":32,"instrument_currency":"EUR","open_transaction_type":"BUY","close_transaction_type":null},{"id":299834,"open_date":"2023-02-06","close_date":null,"open_price":"115","close_price":null,"quantity":50,"transaction_costs":0,"instrument_id":32,"instrument_currency":"EUR","open_transaction_type":"BUY","close_transaction_type":null},{"id":299841,"open_date":"2023-04-12","close_date":"2024-07-10","open_price":"1527","close_price":"1635.5","quantity":129,"transaction_costs":0,"instrument_id":21289,"instrument_currency":"SEK","open_transaction_type":"BUY","close_transaction_type":"SELL"},{"id":299842,"open_date":"2024-02-12","close_date":"2024-08-26","open_price":"1275","close_price":"1763","quantity":101,"transaction_costs":0,"instrument_id":21289,"instrument_currency":"SEK","open_transaction_type":"BUY","close_transaction_type":"SELL"},{"id":299843,"open_date":"2023-04-12","close_date":"2024-08-26","open_price":"1527","close_price":"1763","quantity":71,"transaction_costs":0,"instrument_id":21289,"instrument_currency":"SEK","open_transaction_type":"BUY","close_transaction_type":"SELL"},{"id":299844,"open_date":"2024-02-12","close_date":null,"open_price":"1275","close_price":null,"quantity":36,"transaction_costs":0,"instrument_id":21289,"instrument_currency":"SEK","open_transaction_type":"BUY","close_transaction_type":null},{"id":299845,"open_date":"2023-05-19","close_date":null,"open_price":"0.2192","close_price":null,"quantity":1823,"transaction_costs":0,"instrument_id":21290,"instrument_currency":"DKK","open_transaction_type":"BUY","close_transaction_type":null}]'
    # json_str =('[{"id":299825,"open_date":"2024-10-25","close_date":"2024-11-06","open_price":"90.515","close_price":"160","quantity":35,"transaction_costs":0,"instrument_id":10256,"instrument_currency":"USD","open_transaction_type":"BUY","close_transaction_type":"SELL"},'
    #           '{"id":299826,"open_date":"2024-11-05","close_date":null,"open_price":"80","close_price":null,"quantity":50,"transaction_costs":0,"instrument_id":10256,"instrument_currency":"USD","open_transaction_type":"BUY","close_transaction_type":null},)'
    #            '{"id":299841,"open_date":"2024-11-03","close_date":"2024-11-09","open_price":"100","close_price":"200","quantity":129,"transaction_costs":0,"instrument_id":21289,"instrument_currency":"SEK","open_transaction_type":"BUY","close_transaction_type":"SELL"}]')


    def setUp(self):
        pass

    def test_dates(self):
        #case 1: open_date > start_date, close_date < end_date
        start_date = date(2024, 10, 20)
        end_date = date(2024, 11, 8)
        open_date = date(2024, 10, 25)
        close_date = date(2024, 11, 6)
        po = Position(id=1, open_date=open_date, open_price=150, quantity=100)
        po.start_date = start_date
        po.end_date = end_date
        report_length = (close_date - open_date).days + 1
        po.close_price = 200
        po.close_date = close_date
        po.instrument_currency = 'USD'
        po.init_dates()
        self.assertEqual(len(po.dates), report_length)
        self.assertEqual(po.dates[0], open_date)
        self.assertEqual(po.dates[-1], close_date)
        #case 2: open_date > start_date, close_date is none
        po = Position(id=1, open_date=open_date, open_price=150, quantity=100)
        po.start_date = start_date
        po.end_date = end_date
        po.init_dates()
        report_length = (end_date - open_date).days + 1
        self.assertEqual(len(po.dates), report_length)
        self.assertEqual(po.dates[0], open_date)
        self.assertEqual(po.dates[-1], end_date)
        #case 3: open_date > start_date, close_date > end_date
        po = Position(id=1, open_date=open_date, open_price=150, quantity=100)
        po.start_date = start_date
        po.end_date = end_date
        po.close_date = date(2024, 11, 20)
        po.init_dates()
        report_length = (end_date - open_date).days + 1
        self.assertEqual(len(po.dates), report_length)
        self.assertEqual(po.dates[0], open_date)
        self.assertEqual(po.dates[-1], end_date)
        #case 4: open_date < start_date, close_date < end_date
        po = Position(id=1, open_date=open_date, open_price=150, quantity=100)
        start_date = date(2024, 11 ,1)
        po.start_date = start_date
        po.end_date = end_date
        po.close_date = date(2024, 11, 20)
        po.init_dates()
        report_length = (end_date - start_date).days + 1
        self.assertEqual(len(po.dates), report_length)
        self.assertEqual(po.dates[0], start_date)
        self.assertEqual(po.dates[-1], end_date)
        #case 5: open_date < start_date, close_date > end_date
        po = Position(id=1, open_date=open_date, open_price=150, quantity=100)
        start_date = date(2024, 11 ,1)
        end_date = date(2024, 11, 10)
        po.start_date = start_date
        po.end_date = end_date
        po.close_date = date(2024, 11, 20)
        po.init_dates()
        report_length = (end_date - start_date).days + 1
        self.assertEqual(len(po.dates), report_length)
        self.assertEqual(po.dates[0], start_date)
        self.assertEqual(po.dates[-1], end_date)

    def test_rpp(self):
        open_date = date(2024, 11, 1)
        close_date = date(2024, 11, 5)
        start_date = date(2024, 10, 31)
        end_date = date(2024, 11, 6)
        open_price = 90
        close_price = 115
        prices = [100, 110, 120, 100, 110]
        rates = [1] * 5
        quantity = 100
        # case 1-1: open_price != open day price, close_price != close day price
        po = create_position(id=1, open_date=open_date, close_date=close_date,
                                  start_date=start_date, end_date=end_date,
                                  open_price=open_price, close_price=close_price,
                                  quantity=quantity)
        self.assertEqual(po.start_date, open_date)
        self.assertEqual(po.end_date, close_date)
        po.target_rates = rates
        po.fill_prices(prices)
        po.fill_values()
        po.cal_returns()
        self.assertEqual(po.open_day_price, 100)
        # price[0] should be the open price: 90
        self.assertEqual(po.prices[0], 90)
        # price[-1] should be the close price: 115
        self.assertEqual(po.prices[-1], 115)
        # RPP
        self.assertEqual(po.target_rpp[0], 1000)
        self.assertEqual(po.target_rpp[1], 1000)
        self.assertEqual(po.target_rpp[-1], 1500)
        # RPP%
        self.assertEqual(po.target_rppp[0], 1/9)
        self.assertEqual(po.target_rppp[-1], 0.15)
        # case 1-2: open_date < start_date
        open_date = date(2024, 11, 1)
        close_date = date(2024, 11, 7)
        start_date = date(2024, 11, 2)
        end_date = date(2024, 11, 6)
        open_price = 90
        close_price = 115
        prices = [100, 110, 120, 100, 110]
        rates = [1] * 5
        quantity = 100
        po = create_position(id=1, open_date=open_date, close_date=close_date,
                                  start_date=start_date, end_date=end_date,
                                  open_price=open_price, close_price=close_price,
                                  quantity=quantity)
        self.assertEqual(po.start_date, start_date)
        po.target_rates = rates
        po.fill_prices(prices)
        po.fill_values()
        po.cal_returns()
        # Price
        self.assertEqual(po.prices[0], 100)
        self.assertEqual(po.prices[-1], 110)
        # RPP
        self.assertEqual(po.target_rpp[0], 0)
        self.assertEqual(po.target_rpp[1], 1000)
        self.assertEqual(po.target_rpp[-1], 1000)
        # RPP%
        self.assertEqual(po.target_rppp[0], 0)
        self.assertEqual(po.target_rppp[1], 0.1)
        self.assertEqual(po.target_rppp[-1], 0.1)

