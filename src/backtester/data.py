# %%
import os, os.path 
import pandas as pd

# %%
from abc import ABCMeta, abstractmethod

# %%
from backtester.event import MarketEvent

# %%
class DataHandler(object):
    '''
    DataHandler is a abstract base class which provides and interface
    various other data handlers (both live and historic). 
    
    All child DataHandler object is to output a generated set of bars 
    (OLHCVI) for each symbol requested.

    The process of retrieving the latest bars allows replicates how a live strtagey would work
    and allows the same process to apply for both live and historic trading.  
    '''

    __metaclass__ = ABCMeta

    @abstractmethod
    def get_latest_data(self, symbol, N=1):
        '''
        Returns the N last or fewer bars from the latest_symbol list, 
        or fewer if less bars are available

        Args:
            symbol (string) - symbol for ticker (example 'GOOG')
            N (int, optional) - Number of bars returned, default is 1 
        '''
        raise NotImplementedError('DataHandler child must implement a get_latest_bar() method')
    
    @abstractmethod
    def update_latest_data(self):
        '''
        Pushes the latest bar to the latestes symbol structure for all symbols in the symbol list
        '''
        raise NotImplementedError('DataHandler child must implement a update_bars()')

# %%
class HistoricCSVDataHandler(DataHandler):
    '''
    The HistoricCSVDataHandler is used to read a CSV for each requested symbol
    from memory and provide an interface to obtain 'latest' bar that replicates 
    live trading interface.
    '''

    def __init__(self, events, csv_dir, symbol_list):
        '''
        Initialises the historic data handler from a path to a directory containing the csv files
        and a list of symbols (assuming all files are in the form 'symbol.csv',
        where symbol is a string in the list)

        Args:
            events - The event queue
            csv_dir (str) - Absolute path to the directory containing CSV files.
            symbol_list (List[str]) - A list of symbol strings
        '''
        self.events = events
        self.csv_dir = csv_dir
        self.symbol_list = symbol_list

        self.symbol_data = {}
        self.symbol_dataframe = {}
        self.latest_symbol_data = {}
        self.all_data = {}
        self.continue_backtest = True

        self._open_convert_csv_files()

    def _open_convert_csv_files(self):
        '''
        Open the CSV files from the data directory, converting
        them into pandas DataFrames within a symbol dictionary.

        (Assumes data is from Yahoo)
        '''
        combined_index = None
        
        for symbol in self.symbol_list:
            # Load the CSV file indexed by date (date is index_col 0)
            # construct path to each file
            self.symbol_data[symbol] = pd.read_csv(os.path.join(self.csv_dir, symbol + ".csv"), 
                                                   header = 0, 
                                                   index_col = 0, 
                                                   parse_dates=True)
            
            # Combine the index to pad forward values
            if combined_index is None:
                combined_index = self.symbol_data[symbol].index
            else:
                combined_index.union(self.symbol_data[symbol].index)
                
            self.latest_symbol_data[symbol] = []
            
        for symbol in self.symbol_list:
            self.symbol_dataframe[symbol] = self.symbol_data[symbol].reindex(index=combined_index, method="pad")
            self.all_data[symbol] = self.symbol_dataframe[symbol].copy()
            self.symbol_data[symbol] = self.symbol_dataframe[symbol].iterrows()
            
            
    def _get_new_data(self, symbol):
        """
        Returns the latest bar from the data feed as a tuple.
        """
        for raw_bar in self.symbol_data[symbol]:
            yield tuple([symbol, raw_bar[0], raw_bar[1][0]])
            
    def get_latest_data(self, symbol, N=1):
        """
        Returns the last N bars from the latest_symbol list,
        or N-k if less available.
        """
        try:
            return self.latest_symbol_data[symbol][-N:]
        except KeyError:
            print (f"{symbol} is not available in the historical data set.")

        
    def update_latest_data(self):
        """
        Pushes the latest bar to the latest_symbol_data structure
        for all symbols in the symbol list.
        """
        for symbol in self.symbol_list:
            data = None
            try:
                data = next(self._get_new_data(symbol))
            except StopIteration:
                self.continue_backtest = False
            if data is not None:
                self.latest_symbol_data[symbol].append(data)
        self.events.put(MarketEvent())

# %%
    

# %%
            
