from domain.pmapi.pm_reader import PmReader
from django.conf import settings
import requests
from infrastructure.util.util import date_to_pm_format, EMPTY_FILL_VALUE, date_to_json_str
import json

PM_API_HEADER = {
    "X-Api-Key": settings.PERFORMATIV_API_KEY,
    "candidate_id": settings.PERFORMATIV_API_CANDIDATE_ID
}


class PmReaderImpl(PmReader):

    def read_instrument_prices(self, instrument_id: int, dates: list) -> list:
        url = settings.PERRORMATIV_API_URL_INSTRUMENT_PRICE
        parms = {"instrument_id": str(instrument_id), "start_date": date_to_pm_format(dates[0]),
                 "end_date": date_to_pm_format(dates[-1])}
        r = requests.get(url=url, headers=PM_API_HEADER, params=parms)
        res_dict = r.json()
        data_list = res_dict.get(str(instrument_id))
        # to make sure the return list exactly match the dates' order:
        date_strs = [date_to_json_str(x) for x in dates]
        if data_list:
            mapping = {}
            for item in data_list:
                mapping[item.get('date')] = item.get('price')
            return [mapping.get(dt, EMPTY_FILL_VALUE) for dt in date_strs]
        else:
            raise ValueError("API response does not contain data.")

    def read_fx_rates(self, pair: str, dates: list) -> list:
        url = settings.PERFORMATIV_API_URL_FX_RATE
        parms = {"pairs": pair, "start_date": date_to_pm_format(dates[0]),
                 "end_date": date_to_pm_format(dates[-1])}
        r = requests.get(url=url, headers=PM_API_HEADER, params=parms)
        res_dict = r.json()
        data_list = res_dict.get(pair)
        # to make sure the return list exactly match the dates' order:
        date_strs = [date_to_json_str(x) for x in dates]
        if data_list:
            mapping = {}
            for item in data_list:
                mapping[item.get('date')] = item.get('rate')
            return [mapping.get(dt, EMPTY_FILL_VALUE) for dt in date_strs]
        else:
            raise ValueError("API response does not contain data.")
