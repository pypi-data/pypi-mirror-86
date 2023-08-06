# stock-market
A library that gather stock market historical OHLC data.

# klsescreener

## To get klsescreener dashboard
```
>>> from stock_market.screeners import klsescreener
>>> klsescreener.api.KlseScreener.stocks_screener()
             Name    Code                                    Category  ...  MCap.(M)       Indicators  Unnamed: 15
0       DIGI  [s]    6947     Telecommunications & Media, Main Market  ...  32421.75              NaN           >>
1       MGRC  [s]    0155                     Health Care, Ace Market  ...     64.69              YoY           >>
2         CARLSBG    2836   Consumer Products & Services, Main Market  ...   7117.81              NaN           >>
3    CHINAETF-USD  0829EB                             ETF-Equity, ETF  ...      0.62              NaN           >>
4    LAGENDA  [s]    7179                       Property, Main Market  ...    575.35          QoQ YoY           >>
..            ...     ...                                         ...  ...       ...              ...          ...
977    HUAAN  [s]    2739                         Energy, Main Market  ...    137.79              NaN           >>
978    SEERS  [s]   03009   Consumer Products & Services, Leap Market  ...     25.76             RQoQ           >>
979           M&G    5078     Transportation & Logistics, Main Market  ...     65.15  RQoQ RYoY RTopQ           >>
980  BRAHIMS  [s]    9474   Consumer Products & Services, Main Market  ...     69.70              YoY           >>
981  HHGROUP  [s]    0175  Industrial Products & Services, Ace Market  ...     13.45              NaN           >>

[982 rows x 16 columns]
```

## To export klsescreener dashboard to Excel file
```
>>> from stock_market.screeners import klsescreener
>>> filepath = 'klsescreener.xlsx'
>>> klsescreener.api.export_stocks_screener_to_excel(filepath)
```

# bursamalaysia

## To export securities equities keyindicator PDF
```
>>> from stock_market.screeners import bursamalaysia
>>> bursamalaysia.api.export_securities_equities_keyindicators_pdf('2020-12-31')
```

## To export securities equities PDF
```
>>> from stock_market.screeners import bursamalaysia
>>> bursamalaysia.api.export_securities_equities_pdf('2020-12-31')
```

## To export indices
```
>>> from stock_market.screeners import bursamalaysia
>>> bursamalaysia.api.export_indices_data('0200I')
```

## To export equities
```
>>> from stock_market.screeners import bursamalaysia
>>> bursamalaysia.api.export_equities_data('1818')
```