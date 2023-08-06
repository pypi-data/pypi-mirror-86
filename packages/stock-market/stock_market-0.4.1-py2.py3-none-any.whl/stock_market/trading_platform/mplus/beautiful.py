
# -*- coding: utf-8 -*-

from os.path import abspath, dirname, join
import traceback
import argparse
import inspect
import logging
import json
import sys

import pandas


__THIS = dirname(__file__)

__CONFIG_FILENAME = r'configuration.json'

__CONFIG_FILEPATH = join(__THIS, __CONFIG_FILENAME)

with open(__CONFIG_FILEPATH, 'r') as fh:
    CONTENT = json.load(fh)


class Configuration:

    def get_mapping_between_field_name_and_csv_table_header() -> list:
        '''Get list of information (fields) with respective header .
        '''
        collection = []
        for _, temp in CONTENT.items():
            for k, v in temp.items():
                t = {Configuration.field(): k,
                     Configuration.header(): v}
                collection.append(t)
        return collection

    @staticmethod
    def field() -> str:
        '''Dictionary field name.
        '''
        return inspect.currentframe().f_code.co_name

    @staticmethod
    def header() -> str:
        '''Dictionary field name.
        '''
        return inspect.currentframe().f_code.co_name


class Mplus:

    def __init__(self, filepath) -> object:
        '''Constructor
        '''

        self.filepath = filepath

        logging.info(f'Loading CSV file generated from MPLUS: {filepath}')
        self.dataframe = pandas.read_csv(filepath, encoding='ISO-8859-1')

    def beautify_filepath(self):
        path = self.filepath.replace('.csv', '-beautify.xlsx')
        return path

    def beautify(self) -> None:

        fields_and_headers = Configuration.get_mapping_between_field_name_and_csv_table_header()

        fields, headers = [], []
        for items in fields_and_headers:
            if items[Configuration.header()] in self.dataframe.columns:
                headers.append(items[Configuration.header()])
                fields.append(items[Configuration.field()])
        
        self.dataframe = self.dataframe[headers]  # Arrange columns according header list

        self.dataframe.columns = fields  # Rename headers

        # Beautified csv and xlsx file
        logging.info(f'Exporting result (XLSX beautified) to {self.beautify_filepath()}')
        self.dataframe.to_excel(self.beautify_filepath(), index=False)


def main(path: str) -> int:

    returncode = 0
    try:
        mplus = Mplus(abspath(path))
        mplus.beautify()
    except Exception as e:
        logging.error(f'Raised exception {type(e)}: {e}')
        traceback.print_tb(e.__traceback__)
        returncode = 1
    finally:
        return returncode


def argparser() -> object:
    parser = argparse.ArgumentParser()
    parser.add_argument('file', default=None, type=argparse.FileType('r', encoding='UTF-8'), help='Csv file exported from mplus screener.')
    args = parser.parse_args()
    return args


def interactive() -> int:
    args = argparser()
    returncode = main(args.file.name)
    return returncode


if __name__ == '__main__':
    returncode = interactive()
    sys.exit(returncode)
