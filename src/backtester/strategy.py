
from abc import ABCMeta, abstractmethod

from backtester.event import SignalEvent, MarketEvent

class Strategy():
    
    __metaclass__ = ABCMeta

    @abstractmethod
    def calculate_signals(self, event):
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

    def __init__(self, data, events):
        '''
        Initialises the buy and hold strategy

        Args:
            data (obj) - The DataHandler object that provides data information
            events (obj) - The Event Queue object
        '''
        self.data = data
        self.symbol_list = self.data.symbol_list
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
                data = self.data.get_latest_data(symbol)[0]
                if data is not None and len(data) > 0:
                    signal = SignalEvent(symbol, data[1], 'LONG')
                    self.events.put(signal)
                    self.bought[symbol] = True

        
