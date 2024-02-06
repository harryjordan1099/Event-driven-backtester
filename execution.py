import datetime
import Queue

from abc import ABCMeta, abstractmethod

from event import FillEvent, OrderEvent

class ExecutionHandler():
    """
    The ExecutionHandler abstract class takes in the OrderEvenbts generated 
    by the portfolio and the ultimate set of Fill objects thata ctually occur 
    in the market.
    
    This abstract class allows for both simulated brokerages and live brokerages to
    be used with the same interface. This means we can backtest in a very similar
    manner to a live trading engine.
    """
    
    __metaclass__ = ABCMeta
    
    @abstractmethod
    
    def execute_order(self, event):
        """
        Takes an order event and executes it, producing a Fill 
        event that gets placed onto the Events queue.
        
        Args:
            event (obj) - An event object with order information. 
        """
        raise Not ImplementedError("ExecutionHandler child must implement execute_order()")
        
class SimulatedExecutionHandler(ExecutionHandler):
    """
    This basic implementation for an execution handler simply converts all order
    objects into their equivalent fill objects automatically.
    
    This is unrealistic as this doesnt take into account:
        - 
        
    """
        