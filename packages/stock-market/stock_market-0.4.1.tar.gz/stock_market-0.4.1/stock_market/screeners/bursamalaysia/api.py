
# -*- coding: utf-8 -*-

from abc import ABC, abstractmethod
from datetime import datetime
from enum import Enum, auto
from os.path import join
import logging
import json
import os

from bs4 import BeautifulSoup
import requests


def write_json_file(data: dict, filepath: str, mode: str = 'w', indent: int = 4):
    with open(filepath, mode) as fh:
        fh.write(json.dumps(data, indent=indent))


class DataResolutionType(Enum):
    intraday = auto()
    historical = auto()


class BursaMalaysia(ABC):

    '''Bursa Malaysia utilities.'''

    def __init__(self, stockcode: str) -> object:
        '''Constructor
        '''
        self.stockcode = stockcode

        self.data_api_source = ''
        self.data_stock_code = ''
        self.data_ws_a = ''
        self.data_ws_m = ''
        self.attribs = {}

    def get_web_json_content(self, url: str) -> dict:
        '''Return web content in json format.
        '''
        response = requests.get(url)
        response.raise_for_status()
        content = response.json()
        return content

    def get_intraday(self, fromdate: str = '19820104') -> dict:
        url = f'https:{self.data_api_source}?stock_code={self.data_stock_code}'
        url = f'{url}&mode=intraday&from_date={fromdate}&ws_a={self.data_ws_a}&ws_m={self.data_ws_m}'
        logging.debug(f'Visiting its api page \'{self.stockcode}\': {url}')

        content = self.get_web_json_content(url)
        return content

    def get_historical(self, fromdate: str = '19820104') -> dict:
        url = f'https:{self.data_api_source}?stock_code={self.data_stock_code}'
        url = f'{url}&mode=historical&from_date={fromdate}&ws_a={self.data_ws_a}&ws_m={self.data_ws_m}'
        logging.debug(f'Visiting its api page \'{self.stockcode}\': {url}')

        content = self.get_web_json_content(url)
        return content

    def intraday_filename(self, filename_prefix=None):
        filename = f'{filename_prefix}-intraday.json' if filename_prefix else f'{self.stockcode}-intraday.json'
        return filename

    def historical_filename(self, filename_prefix=None):
        filename = f'{filename_prefix}-historical.json' if filename_prefix else f'{self.stockcode}-historical.json'
        return filename

    @staticmethod
    def url() -> str:
        '''Bursa Malaysia url'''
        return 'https://www.bursamalaysia.com/'

    @staticmethod
    def listing_directory_url() -> str:
        '''Bursa Malaysia listing directory url'''
        return f'{BursaMalaysia.url()}/trade/trading_resources/listing_directory/'

    @staticmethod
    def beautify_content(content: dict, resolution: str) -> dict:

        result = {}

        content = content.values()
        content = list(content)[0]['data']

        for d in content:

            timestamp = d['date'] // 1000
            date = datetime.fromtimestamp(timestamp)

            d['timestamp'] = timestamp
            d['resolution'] = resolution
            d['date'] = str(date.date())
            d['time'] = str(date.time())
            result[timestamp] = d

        return result

    def intraday_beautify_filename(self, filename_prefix=None):
        filename = f'{filename_prefix}-intraday-beautify.json' if filename_prefix else f'{self.stockcode}-intraday-beautify.json'
        return filename

    def historical_beautify_filename(self, filename_prefix=None):
        filename = f'{filename_prefix}-historical-beautify.json' if filename_prefix else f'{self.stockcode}-historical-beautify.json'
        return filename

    @abstractmethod
    def get_webpage_div_attribute(self, url: str) -> None:
        '''Get webpage attributes
        '''
        response = requests.get(url)
        response.raise_for_status()
        tree = BeautifulSoup(response.content, 'html5lib')
        stockchart_container = tree.find('div', attrs={'id': 'stockChartContainer'})
        self.attribs = stockchart_container.attrs
        self.data_api_source = self.attribs['data-api-source']
        self.data_stock_code = self.attribs['data-stock-code']
        self.data_ws_a = self.attribs['data-ws-a']
        self.data_ws_m = self.attribs['data-ws-m']


class Equities(BursaMalaysia):

    def __init__(self, stockcode):
        '''Constructor'''
        super().__init__(stockcode)
        self.get_webpage_div_attribute()

    def get_webpage_div_attribute(self):
        '''Setup webpage attributes'''
        url = self.listing_directory_url()
        url = f'{url}company-profile?stock_code={self.stockcode}'
        logging.debug(f'Visiting equities code \'{self.stockcode}\' page: {url}')

        super().get_webpage_div_attribute(url)
        logging.debug(f'Return page attributes: {self.attribs}')


class Indices(BursaMalaysia):

    def __init__(self, stockcode):
        '''Constructor'''
        super().__init__(stockcode)
        self.get_webpage_div_attribute()

    def get_webpage_div_attribute(self):
        '''Setup webpage attributes'''
        url = self.listing_directory_url()
        url = f'{url}indices-profile?stock_code={self.stockcode}'
        logging.debug(f'Visiting equities code \'{self.stockcode}\' page: {url}')

        super().get_webpage_div_attribute(url)
        logging.debug(f'Return page attributes: {self.attribs}')


def export_equities_data(stockcode: str, basefolder: str = os.getcwd(), filename_prefix=None, fromdate: str = '19820104') -> int:

    try:
        e = Equities(stockcode)

        # Export raw data
        intraday_data = e.get_intraday(fromdate)
        historical_data = e.get_historical(fromdate)
        # write_json_file(intraday_data, join(basefolder, e.intraday_filename(filename_prefix)))
        # write_json_file(historical_data, join(basefolder, e.historical_filename(filename_prefix)))

        # Export beautify data
        intraday_beautify_data = e.beautify_content(intraday_data, DataResolutionType.intraday.name)
        historical_beautify_data = e.beautify_content(historical_data, DataResolutionType.historical.name)
        write_json_file(intraday_beautify_data, join(basefolder, e.intraday_beautify_filename(filename_prefix)))
        write_json_file(historical_beautify_data, join(basefolder, e.historical_beautify_filename(filename_prefix)))

        return 0

    except Exception as e:
        logging.error(f'Failed to export equities {stockcode} data due to reason {e}')
        return 1


def export_indices_data(stockcode: str, basefolder: str = os.getcwd(), filename_prefix=None, fromdate: str = '19820104') -> int:

    try:
        i = Indices(stockcode)

        # Export raw data
        intraday_data = i.get_intraday(fromdate)
        historical_data = i.get_historical(fromdate)
        # write_json_file(intraday_data, join(basefolder, i.intraday_filename(filename_prefix)))
        # write_json_file(historical_data, join(basefolder, i.historical_filename(filename_prefix)))

        # Export beautify data
        intraday_beautify_data = i.beautify_content(intraday_data, DataResolutionType.intraday.name)
        historical_beautify_data = i.beautify_content(historical_data, DataResolutionType.historical.name)
        write_json_file(intraday_beautify_data, join(basefolder, i.intraday_beautify_filename(filename_prefix)))
        write_json_file(historical_beautify_data, join(basefolder, i.historical_beautify_filename(filename_prefix)))

        return 0

    except Exception as e:
        logging.error(f'Failed to export indices {stockcode} data due to reason {e}')
        return 1
