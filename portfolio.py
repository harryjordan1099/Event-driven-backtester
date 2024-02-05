import datetime
import numpy as np
import pandas as pd
import Queue

from abc import ABCMeta, abstractmethod
from math import floor

from event import FillEvent, OrderEvent

class Portfolio():
    """
    The Portfolio abstract class acts on signals from the SignalEvent 
    to generate orders and updates the current positions and holdings from a 
    FillEvent. It handles this at a resolution of a "bar" (1 second, 1 min,
    5-min, 30-min, 60-min or EOD).
    """
    
    __metaclass__ = ABCMeta
    
    @abstractmethod
    def update_signal(self, event):
        """
        Acts on a SignalEvent to generate new orders
        based on the portfolio logic.
        """
        raise NotImplementedError("Portfolio child must implement update_signal() method")
        
    @abstractmethod
    def update_fill(self, event):
        """
        Updates the portfolio current positions and holdings
        from a fill event.
        """
        raise NotImplementedError("Portfolio child must implement update_fill() method")
        
class NaivePortfolio(Portfolio):
    """
    The NaivePortfolio object is a Basic Portfolio object. It is "Naive" because it sends the 
    order to the a brokerage object with a constant quantity size blindly without risk management
    or position sizing. 
    """
    
    def __init__(self, bars, events, start_date, initial_capital=100000.0):
        """
        Initialises the portfolio.
        
        Args:
        - bars (obj) - The DataHandler object with current market data.
        - events (obj) - The Event Queue object.
        - start_date - The start date (bar) of the portfolio.
        - initial_capital (float) - The starting capital in USD
        """
        self.bars = bars
        self.events = events
        self.symbol_list = self.bars.symbol_list
        self.start_date = start_date
        self.initial_capital = initial_capital
        
        self.all_positions = self.construct_all_positions()
        self.current_positions = {symbol: 0 for symbol in self.symbol_list}
        
        self.all_holdings = self.construct_all_holdings()
        self.current_holdings = self.construct_current_holdings()
        
    def construct_all_positions(self):
        """
        Constructs the positions list using the start_date
        to determine when the time index will begin.
        """
        positions = {symbol: 0 for symbol in self.symbol_list}
        positions["datestamp"] = self.start_date
        return positions
    
    def construct_all_holdings(self):
        """
        Constructs the holdings list using the start_date
        to determine when the time index will begin.
        """
        holdings = {symbol: 0 for symbol in self.symbol_list}
        holdings["datestamp"] = self.start_date
        holdings["cash"] = self.initial_capital
        holdings["commission"] = 0.0
        holdings["total"] = self.initial_capital
        return holdings
    
    def calculate_current_holdings(self):
        """
        This constructs the dictionary which will hold the instantaneous 
        value of the portfolio across all symbols.
        """
    
    