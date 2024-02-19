import time
import queue

from datetime import datetime
from event import MarketEvent, SignalEvent, OrderEvent, FillEvent
from data import HistoricCSVDataHandler
from strategy import BuyAndHoldStrategy
from portfolio import NaivePortfolio
from execution import SimulatedExecutionHandler

def backtest(events, data, portfolio, strategy, broker):
    while True:
        data.update_bars()
        if data.continue_backtest == False:
            break
            
        while True:
            try:
                event = events.get(block=False)
            except queue.Empty:
                break
            
            if event is not None:
                if event.type == "MARKET":
                    strategy.calculate_signals(event)
                    portfolio.update_timeindex(event)
                elif event.type == "SIGNAL":
                    portfolio.update_signal(event)
                elif event.type == "ORDER":
                    broker.execute_order(event)
                elif event.type == "FILL":
                    portfolio.update_fill(event)
                    
    stats = portfolio.output_summary_stats()
    
    for stat in stats:
        print(stat[0] + ": " stat[1])
        
events = queue.Queue()
data = HistoricCSVDataHandler(events, 'csv/', ['OMXS30'], DataSource.NASDAQ)
portfolio = NaivePortfolio(data, events, '', initial_capital=2000)
strategy = MovingAveragesLongStrategy(data, events, portfolio, 50, 100, version=1)
portfolio.strategy_name = strategy.name
broker = SimulateExecutionHandler(events)

backtest(events, data, portfolio, strategy, broker)
    
            