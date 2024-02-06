import numpy as np
import pandas as pd

def create_sharpe_ratio(returns, N=252):
    """
    Calculate the annualised Sharpe ratio of a returns stream
    based on a number of trading periods, N. N defaults to 252
    as there are 252 trading days in a year. 
    
    This also assumes a benchmark of zero (calculating the 
    risk-adjusted return)
    
    Args:
        return (pd.series) - A pandas Series that represents the 
            period percentage returns.
        periods (float) -  Daily (252), Hourly (252*6.5), 
            Minutely (252*6.5*60) etc.
    """
    return np.sqrt(periods) * (np.mean(returns)) / np.std(returns)
    
def create_drawdowns(equity_curve):
    """
    Calculate the maximum peak-to-trough drawdown of PnL curve
    as well as the duration of the drawdown.
    
    Args:
        equity_curve (pd.series) - A pandas Series that represents the 
            period percentage returns.
    Returns:
        drawdown (