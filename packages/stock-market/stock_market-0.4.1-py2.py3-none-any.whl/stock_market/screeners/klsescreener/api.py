
# -*- coding: utf-8 -*-

import logging

import pandas
import requests


class KlseScreener:

    '''KLSE Screener utilities.'''

    @staticmethod
    def url() -> str:
        '''KLSE Screener url'''
        return 'https://www.klsescreener.com/v2/'

    @staticmethod
    def stocks_api_url() -> str:
        '''Stocks api url'''
        return 'https://www.klsescreener.com/v2/screener/quote_results'

    @staticmethod
    def warrants_api_url() -> str:
        '''Warrants api url'''
        return 'https://www.klsescreener.com/v2/screener_warrants/quote_results'

    @staticmethod
    def stocks_screener() -> pandas.DataFrame:
        '''Stocks screener'''
        url = KlseScreener.stocks_api_url()
        return KlseScreener.__request_url(url)

    @staticmethod
    def warrants_screener() -> pandas.DataFrame:
        '''Warrants screener.
        Remark: Only return first 100 rows of record.
        '''
        url = KlseScreener.warrants_api_url()
        return KlseScreener.__request_url(url)

    @staticmethod
    def __request_url(url: str) -> pandas.DataFrame:
        '''Private method to retrieve api url content.'''
        response = requests.get(url)
        response.raise_for_status()
        dataframe = pandas.read_html(response.text)
        dataframe = dataframe[0]
        return dataframe


def export_stocks_screener_to_excel(path: str) -> int:
    '''Export stocks screener to excel .xlsx file'''

    returncode = 0

    try:
        dataframe = KlseScreener.stocks_screener()
        dataframe.to_excel(path, index=False)
    except Exception as e:
        logging.error(e)
        returncode = 1
    finally:
        return returncode
