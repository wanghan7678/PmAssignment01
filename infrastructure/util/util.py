from datetime import date, datetime, timedelta

PM_DATE_FORMAT = "%Y%m%d"
JSON_DATE_FORMAT = "%Y-%m-%d"
EMPTY_FILL_VALUE = 0


def date_to_pm_format(input_date: date) -> str:
    return input_date.strftime(PM_DATE_FORMAT)


def json_str_to_date(input_date_str: str) -> date:
    if input_date_str is None:
        return None
    return datetime.strptime(input_date_str, JSON_DATE_FORMAT).date()


def date_to_json_str(input_date: date) -> str:
    return input_date.strftime(JSON_DATE_FORMAT)


def generate_date_list(start_date: date, end_date: date):
    days: int = (end_date - start_date).days + 1
    return [start_date + timedelta(days=i) for i in range(days)]


def to_float(input_value):
    if input_value:
        return float(input_value)
    return None


def remove_leading_trailing_zeros(lst):
    leading_zeros = 0
    for num in lst:
        if num == 0:
            leading_zeros += 1
        else:
            break
    trailing_zeros = 0
    for num in reversed(lst):
        if num == 0:
            trailing_zeros += 1
        else:
            break

    if leading_zeros + trailing_zeros >= len(lst):
        result = []
    else:
        result = lst[leading_zeros:len(lst) - trailing_zeros]

    return result, leading_zeros, trailing_zeros

def remove_leading_zeros(lst):
    leading_zeros = 0
    for num in lst:
        if num == 0:
            leading_zeros += 1
        else:
            break
    if leading_zeros >= len(lst):
        result = []
    else:
        result = lst[leading_zeros:]
    return result, leading_zeros


def fill_empty(dates: list, values: list, value_start: date, value_end: date) -> list:
    if len(dates) == len(values):
        return values
    results = [0] * len(dates)
    start_index = dates.index(value_start)
    end_index = dates.index(value_end)
    for i in range(start_index, end_index + 1):
        if i < len(dates):
            results[i] = values[i - start_index]
    return results