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
            bars (obj) - The DataHandler object with current market data.
            events (obj) - The Event Queue object.
            start_date - The start date (bar) of the portfolio.
            initial_capital (float) - The starting capital in USD
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
    
    def construct_current_holdings(self):
        """
        This constructs the dictionary which will hold the instantaneous 
        value of the portfolio across all symbols.
        """
        holdings = {symbol:0 for symbol in self.symbol_list}
        holdings["cash"] = self.initial_capital
        holdings["commission"] = 0
        holdings["total"] = self.initial_capital
        return holdings
    
    def update_timeindex(self, event):
        """
        Adds a new record to the all_positions matrix for the current market
        data bar. This reflects the PREVIOUS bar, i.e. all current market data 
        at this stage is known (OHLCVI). 
        
        Makes use of a MarketEvent from the events queue.
        """
        bars = {
            symbol: self.bars.get_latest(data, symbol)
            for symbol in self.symbol_list
        }
        
        # positions 
        positions = {
            symbol: self.current_positions[symbol]
            for symbol in self.symbol_list
        }
        
        # Append the current positions
        datestamp = bars[self.symbol_list[0]][0][1]
        positions["datestamp"] = datestamp
        self.all_positions.append(positions)
        
        # Update holdings
        holdings = {symbol: 0 for symbol in self.symbol_list}
        holdings['datestamp'] = datestamp
        holdings['cash'] = self.current_holdings['cash']
        holdings['commission'] = self.current_holdings['commission']
        holdings['total'] = self.current_holdings['cash']
        
        for symbol in self.symbol_list:
            # Approximation to real value, this is sufficient for Intraday
            # trading but not for daily strategies as opening prices can
            # differ substantially from the closing price
            market_value = self.current_positions[symbol] * bar[symbol][0][5]
            holdings[symbol] = market_value
            holdings["total"] += market_value
            
        self.all_holdings.append(holdings)
        
    def update_positions_from_fill(self, fill):
        """
        Determines whether a FillEvent is either a Buy
        or Sell and then updates the current_positions dictionary accordingly by
        adding/subtracting the correct quantity of shares.
        
        Args:
            fill(obj) - The FillEvent object to update the posiitons with.
        """
        # kinda safe, would fail if not "BUY" or "SELL"
        direction = 1 if event.direction == 'BUY' else -1
        self.current_positions[event.symbol] += copysign(event.quantity, direction)
         
    def update_holdings_from_fill(self, fill):
        """
        Determines a FillEvent is either a Buy or Sell ands then updates
        the current_holdings dictionary 
        
        Args:
            fill (obj) - The FillEvent object to update the posiitons with.
        """
        # kinda safe, would fail if not "BUY" or "SELL"
        direction = 1 if event.direction == 'BUY' else -1
        
        # Update holdings list with new quantities.
        fill_cost = self.bars.get_latest_bars(fill.symbol)[0][5] # Close price
        cost = fill_dir * fill_cost * fill.quantity
        self.current_holdings[fill.symbol] += cost
        self.current_holdings["commission"] += fill.commission
        self.current_holdings["cash"] -= cost + fill.commission 
        self.current_holdings["total"] -= cost + fill.commission
        
    def update_fill(self, event):
        """
        Updates the portfolio current positions and holdings 
        from a FillEvent.
        """
        if event.type == "FILL":
            self.update_positions_from_fill(event)
            self.update_holdings_from_fill(event)
            
    def generate_naive_order(self, signal):
        """
        Simply transacts an Orderevent object as a constant quantity 
        sizing of the signal object (100 shares), without risk management or
        position sizing considerations. 
        
        Args:
            signal (obj) - The SignalEvent signal information
        """
        if isinstance(event, SignalEvent)
                    direction = 'BUY' if event.signal_type == 'LONG' else 'SELL'
                    return OrderEvent(
                        event.symbol,
                        'MARKET',
                        100,
                        direction
                    )
                