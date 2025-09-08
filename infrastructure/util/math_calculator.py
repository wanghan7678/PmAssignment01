from infrastructure.util.util import remove_leading_trailing_zeros

NUMBER_OF_DECIMALS = 8


def get_return_list(value_list: [], open_type="BUY") -> []:
    cal_list, leading, trailing = remove_leading_trailing_zeros(value_list)
    R = [0] + [round((cal_list[i] - cal_list[i - 1]), NUMBER_OF_DECIMALS) for i in range(1, len(cal_list))]
    RP = [0] + [round((cal_list[i] - cal_list[i - 1]) / cal_list[i - 1], NUMBER_OF_DECIMALS + 2)
                if cal_list[i - 1] != 0
                else 0
                for i in
                range(1, len(cal_list))]
    if open_type == "SELL":
        R = [-x for x in R]
        RP = [-x for x in RP]
    R = [0] * leading + R + [0] * trailing
    RP = [0] * leading + RP + [0] * trailing
    return R, RP




