
# -*- coding: utf-8 -*-

import requests
import pandas


def get_latest_quarter_result():
    url = 'https://klse.i3investor.com/financial/quarter/latest.jsp'
    response = requests.get(url, stream=True, headers={'User-agent': 'Mozilla/5.0'})
    dataframe = pandas.read_html(response.content, match='Ann. Date')
    dataframe = dataframe[-1]
    return dataframe


def get_latest_annual_result():
    url = 'https://klse.i3investor.com/financial/annual/latest.jsp'
    response = requests.get(url, stream=True, headers={'User-agent': 'Mozilla/5.0'})
    dataframe = pandas.read_html(response.content, match='Financial Year', skiprows=1)
    dataframe = dataframe[-1]
    return dataframe


def get_upcoming_quarter_result():
    url = 'https://klse.i3investor.com/financial/quarter/upcoming.jsp'
    response = requests.get(url, stream=True, headers={'User-agent': 'Mozilla/5.0'})
    dataframe = pandas.read_html(response.content, match='Latest Quarter')
    dataframe = dataframe[-1]
    return dataframe


def get_upcoming_annual_result():
    url = 'https://klse.i3investor.com/financial/annualReport/upcoming.jsp'
    response = requests.get(url, stream=True, headers={'User-agent': 'Mozilla/5.0'})
    dataframe = pandas.read_html(response.content, match='Latest F.Y.')
    dataframe = dataframe[-1]
    return dataframe


def get_price_target_table():
    url = 'http://klse.i3investor.com/jsp/pt.jsp'
    response = requests.get(url, stream=True, headers={'User-agent': 'Mozilla/5.0'})
    dataframe = pandas.read_html(response.content, match='Stock Name')
    dataframe = dataframe[-1]
    return dataframe

