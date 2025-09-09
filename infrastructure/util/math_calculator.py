from infrastructure.util.util import remove_leading_trailing_zeros, remove_leading_zeros
import logging
logger = logging.getLogger(__name__)
logging.basicConfig(filename='myapp.log', level=logging.INFO)

NUMBER_OF_DECIMALS = 8

def get_returns(value_list: list, open_type="BUY", open_day_value=None) -> list:
    R = [0] + [(value_list[i] - value_list[i-1]) for i in range(1, len(value_list))]
    RP = [0] + [(value_list[i] - value_list[i-1]) / value_list[i-1]
                if value_list[i-1] != 0
                else 0
                for i in
                range(1, len(value_list))
                ]
    if open_day_value and value_list[0] != 0:
        R[0] = (open_day_value - value_list[0])
        RP[0] = (R[0] / value_list[0])
    if open_type == "SELL":
        R = [-x for x in R]
        RP = [-x for x in RP]
    return R, RP


def get_round(input_value):
    return round(input_value, NUMBER_OF_DECIMALS)

