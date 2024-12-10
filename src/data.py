"""
Module for fetching and processing historical stock and ETF data from Yahoo Finance.

This module provides functions to retrieve and process historical price data
for individual stocks or ETFs,
and to combine data from multiple tickers into a unified DataFrame.

Functions:
----------
- import_data(name, start):
    Fetches and processes historical price data for a single stock or ETF.
- generate_df_from_list(list_etf, starting_time):
    Combines historical data for a list of ETFs into a single DataFrame with a common date range.

Dependencies:
-------------
- pandas
- pandas_datareader
- yfinance
"""

import datetime as dt
from pandas_datareader import data as pdr
import yfinance as yfin


def import_data(name, start):
    """
    Fetches historical stock price data from Yahoo Finance, processes it,
    and returns the adjusted data.

    Parameters:
    ----------
    name : str
        The ticker symbol of the stock to fetch data for (e.g., '^GSPC' for S&P500).
    start : str or datetime
        The start date for the data retrieval in 'YYYY-MM-DD' format or as a `datetime` object.

    Returns:
    -------
    pandas.DataFrame
        A DataFrame containing the stock's closing prices with the index set to the date.
        The DataFrame has a single column labeled with the stock ticker symbol.
    """

    end = dt.datetime.now()
    yfin.pdr_override()
    data = pdr.get_data_yahoo(name, start=start, end=end)
    data.reset_index(inplace=True)
    data.set_index("Date", inplace=True)
    data = data.drop(["Low", "Open", "Adj Close", "High", "Volume"], axis="columns")
    data.columns = [str(name)]
    return data


def generate_df_from_list(list_etf, starting_time):
    """
    Generates a combined DataFrame of historical stock data for a list of ETFs.

    This function retrieves historical data for each ETF in the provided list,
    processes the data, and merges it into a single DataFrame.
    Missing data rows are removed from the final result.

    Parameters:
    ----------
    list_etf : list of str
        A list of ETF ticker symbols to retrieve data for (e.g., ['^GSPC', 'SWDA.MI', 'XGLE.MI']).
    starting_time : str or datetime
        The start date for data retrieval in 'YYYY-MM-DD' format or as a `datetime` object.

    Returns:
    -------
    pandas.DataFrame
        A DataFrame where each column corresponds to the closing prices of an ETF,
        labeled by its ticker symbol.
        Rows with missing data (NaN) across any column are removed.
    """

    dfs = []

    for etf in list_etf:
        dfs.append(import_data(etf, start=starting_time))

    for i, data_frame in enumerate(dfs):
        if i == 0:
            new_df = data_frame
        else:
            new_df = new_df.join(data_frame)

    new_df.dropna(inplace=True)

    return new_df
