
# -*- coding: utf-8 -*-

from os.path import dirname, exists, join
import pandas


__FILENAME = 'Mid_Small_Cap_PLCs__Mkt_cap_of_200_mil_to_2_bil__Dec2019_V3.0.xlsx'

__FILEPATH = join(dirname(__file__), 'bin', __FILENAME)

if not exists(__FILEPATH):
    raise FileNotFoundError(__FILEPATH)

DATAFRAME = pandas.read_excel(__FILEPATH, skiprows=2)


def check_waiver_via_stockcode(stockcode):
    stockcode = str(stockcode)
    df = DATAFRAME[DATAFRAME['Stock Code'].astype(str) == stockcode]
    if df.empty:
        return False
    return True


def check_waiver_via_stockname(stockname):
    df = DATAFRAME[DATAFRAME['Stock Name'] == stockname]
    if df.empty:
        return False
    return True


if __name__ == '__main__':
    value = input('Enter stockcode/stockname: ')
    if value.isdigit():
        status = check_waiver_via_stockcode(value)
        message = f'Stockcode {value} waiver: {status}'
    else:
        status = check_waiver_via_stockname(value)
        message = f'Stockname {value} waiver: {status}'
    print(message)
    
