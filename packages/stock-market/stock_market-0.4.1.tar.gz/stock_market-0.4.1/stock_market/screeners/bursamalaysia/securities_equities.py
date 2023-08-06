
# -*- coding: utf-8 -*-

from os.path import join
import logging
import os

try:
    import api
except ImportError:
    from . import api

import requests


class CommonSecuritiesEquities:

    def __init__(self, date):
        self.date = date

    def _download(self, url, filepath):
        try:
            response = requests.get(url, stream=True, headers={'User-agent': 'Mozilla/5.0'})
            response.raise_for_status()
        except Exception as e:
            logging.error(e)
            return 1

        try:
            open(filepath, 'wb').write(response.content)
            return 0
        except Exception as e:
            logging.error(e)
            return 2

    @staticmethod
    def bursamalaysia_url():
        return api.BursaMalaysia.url()


class SecuritiesEquities(CommonSecuritiesEquities):

    def __init__(self, date):
        super().__init__(date)

    def filename(self):
        filename = f'securities_equities_{self.date}.pdf'
        return filename

    def filepath(self, basepath=os.getcwd()):
        filepath = join(basepath, self.filename())
        return filepath

    def uri(self):
        uri = f'{self.bursamalaysia_url()}misc/missftp/securities/{self.filename()}'
        return uri

    def export(self, basepath=os.getcwd()):
        url = self.uri()
        filepath = self.filepath(basepath)
        returncode = self._download(url, filepath)
        return returncode


class SecuritiesEquitiesKeyindicators(CommonSecuritiesEquities):

    def __init__(self, date):
        super().__init__(date)

    def filename(self):
        filename = f'securities_equities_keyindicators_{self.date}.pdf'
        return filename

    def filepath(self, basepath=os.getcwd()):
        filepath = join(basepath, self.filename())
        return filepath

    def uri(self):
        uri = f'{self.bursamalaysia_url()}misc/missftp/securities/{self.filename()}'
        return uri

    def export(self, basepath=os.getcwd()):
        url = self.uri()
        filepath = self.filepath(basepath)
        returncode = self._download(url, filepath)
        return returncode
