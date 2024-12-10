"""
Module for analyzing stock and ETF data through correlation calculations.

This module provides functions to compute rolling returns and correlation
coefficients over different time windows. It is designed to facilitate the
exploration of relationships between financial instruments.

Functions:
----------
- compute_correlations(data, time_window):
    Computes rolling percentage returns and the correlation coefficient
    between the first two columns of a dataset for a specified time window.
- compute_correlations_in_time(data, time_grid):
    Computes correlation coefficients for a dataset over a range of time
    window sizes.

Dependencies:
-------------
- pandas
- tqdm
- compute_correlations (from the same module)
"""

import pandas as pd
from tqdm import tqdm


def compute_correlations(data, time_window):
    """
    Computes rolling returns and the correlation coefficient between the
    first two columns of a dataset.

    Parameters:
    ----------
    data : pandas.DataFrame
        A DataFrame containing time series data. Each column represents a
        different stock or ETF.
    time_window : int
        The time window (in rows) over which to calculate percentage returns.

    Returns:
    -------
    tuple
        - pandas.DataFrame: A DataFrame of percentage returns with the same
          columns as the input `data`. The index is adjusted for the time
          window.
        - float: The correlation coefficient between the first two columns
          of the percentage returns DataFrame.
    """

    rendimenti = []

    for i in range(0, len(data) - time_window):
        rendimento = 100 * (data.iloc[i + time_window] / data.iloc[i] * 100 - 1)
        rendimenti.append(rendimento)

    df_rendimenti = pd.DataFrame(
        rendimenti, columns=data.columns, index=data.index[0 : len(data) - time_window]
    )

    corr_coeff = df_rendimenti.corr().iloc[1, 0]

    return df_rendimenti, corr_coeff


def compute_correlations_in_time(data, time_grid):
    """
    Computes the correlation coefficient for the first two columns of a
    dataset over a range of time windows.

    Parameters:
    ----------
    data : pandas.DataFrame
        A DataFrame containing time series data. Each column represents a
        different stock or ETF.
    time_grid : list of int
        A list of time window sizes (in rows) over which to calculate
        percentage returns and their correlation.

    Returns:
    -------
    tuple
        - list of int: The input `time_grid`, representing the time window
          sizes.
        - list of float: Correlation coefficients for each time window in
          `time_grid`.
    """

    corr_grid = []

    for i in tqdm(range(len(time_grid))):
        corr_grid.append(compute_correlations(data, time_window=time_grid[i])[1])

    return time_grid, corr_grid
