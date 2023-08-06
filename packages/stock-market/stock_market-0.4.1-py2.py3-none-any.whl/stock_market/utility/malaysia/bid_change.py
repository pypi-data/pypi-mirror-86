
# -*- coding: utf-8 -*-

from os.path import dirname, exists, join
import json


__FILENAME = 'bid_changes.json'

__FILEPATH = join(dirname(__file__), 'bin', __FILENAME)

if not exists(__FILEPATH):
    raise FileNotFoundError(__FILEPATH)

CONFIG = json.load(open(__FILEPATH, 'r'))


def get_bid_change(start_price, stop_price):
    stop_index = CONFIG.index(stop_price)
    start_index = CONFIG.index(start_price)
    bid_change = stop_index - start_index
    return bid_change
