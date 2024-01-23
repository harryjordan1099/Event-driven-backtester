import datetime
import os, os.path 
import pandas as pd

from abc import ABCMeta, abstractmethod

from event import MarketEvent

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
    def get_latest_bars(self, symbol, N=1):
        '''
        Returns the N last or fewer bars from the latest_symbol list, 
        or fewer if less bars are available

        Args:
            symbol (string) - symbol for ticker (example 'GOOG')
            N (int, optional) - Number of bars returned, default is 1 
        '''
        raise NotImplementedError('DataHandler child must implement a get_latest_bar() method')
    
    @abstractmethod
    def update_bars(self):
        '''
        Pushes the latest bar to the latestes symbol structure for all symbols in the symbol list
        '''
        raise NotImplementedError('DataHandler child must implement a update_bars()')
    
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
        self.latest_symbol_data = {}
        self.continue_backtest = True

        self._open_convert_csv_files()

    def _open_convert_csv_files(self):
        '''
        Open the CSV files from the data directory, converting
        them into pandas DataFrames within a symbol dictionary.

        (Assumes data is from Yahoo)
        '''
        comb_index = None

        for s in self.symbol_list:
            # Load the CSV file indexed by date (date is index_col 0)
            self.symbol_data[s] = pd.read_csv(
                #construct path to
                os.path.join(self.csv_dir, f'{s}.csv'),
                header=0, index_col=0, parse_dates=True,
                names = [
                    'datetime', 'open', 'high',
                    'low', 'close', 'adj_close', 'volume'
                ]
            )
            self.symbol_data[s].sort_index(inplace=True)

            # Combine the index to pad forward values
            if comb_index is None:
                comb_index = self.symbol_data[s].index
            else:
                comb_index.union(self.symbol_data[s].index)

            # Set the latest symbol_data to None
            self.latest_symbol_data[s] = []

        for s in self.symbol_list:
            self.symbol_data[s] = self.symbol_data[s].reindex(
                index=comb_index, method='pad'
            )
            self.symbol_data[s]['returns'] = self.symbol_data[s]['adj_close'].pct_change().dropna()
            self.symbol_data[s] = self.symbol_data[s].iterrows()

        # Reindex the dataframes
        for s in self.symbol_list:
            self.symbol_data[s] = self.symbol_data[s].reindex(index=comb_index, method='pad').iterrows()

            