import datetime
import numpy as np
import pandas as pd
import Queue

from abc import ABCMeta, abstractmethod

from event import SignalEvent, MarketEvent

class Strategy():
    
    __metaclass__ = ABCMeta

    @abstractmethod
    def calculate_signals(self):
        '''
        Abstract method that calculates the list of signals
        '''
        raise NotImplementedError('Strategy child must implement calculate_signals() method')
    

class BuyAndHoldStrategy(Strategy):
    '''
    This strategy simply goes LONG all of the time as soon as a bar is received and will
    never exit a position.

    This is will be used to compare the performance of other strategies and for testing.
    '''

    def __init__(self, bars, events):
        '''
        Initialises the buy and hold strategy

        Args:
            bars (obj) - The DataHandler object that provides bar information
            events (obj) - The Event Queue object
        '''
        self.bars = bars
        self.symbol_list = self.bars.symbol_list
        self.events = events

        # As soon as the buy and hold signal is given, these are set to True
        # This allows the strategy to know whether it is 'In the market' or not
        self.bought = {symbol: False for symbol in self.symbol_list}

    def calculate_signals(self, event):
        '''
        For 'Buy and Hold', we generate a single signal for each symbol
        to buy and thats it. Therefore we are constantly long from the date
        of strategy initialisation.

        Args:
            event(obj) - a MarketEvent object.
        '''
        if isinstance(event, MarketEvent):
            for symbol in self.symbol_list:
                bars = self.bars.get_latest_bars(symbol)[0]
                if bars is not None and len(bars) > 0:
                    signal = SignalEvent(symbol, bars[1], 'LONG')
                    self.events.put(signal)
                    self.bought[symbol] = True

        
