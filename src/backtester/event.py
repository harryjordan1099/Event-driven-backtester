from typing import Any


class Event:
    """
    This is the Parent class for all other subsequent (inheritted) event classes. These
    events will be used to communicate information between projects.  
    """

    pass


class MarketEvent(Event):
    """
    Handles the event of receiving a new market update with corresponding bars.
    """

    def __init__(self):
        """
        Initialises the MarketEvent.
        """
        self.type = "MARKET"


class SignalEvent(Event):
    """
    This Event corresponds to sending a signal from a Strategy object to a Portfolio object and then acted upon.
    """

    def __init__(self, symbol, datetime, signal_type):
        """
        Initialises the SignalEvent.

        Args:
            symbol (str) - The ticker symbol e.g. 'GOOG'
            datetime - The timestamp at which the signal was generated
            signal_type (str) - 'LONG' or 'SHORT'
        """

        self.type = "SIGNAL"
        self.symbol = symbol
        self.datetime = datetime
        self.signal_type = signal_type


class OrderEvent(Event):
    """
    This event corresponds to sending an Order to an execution system.
    The order will contain a symbol (e.g. GOOG), a type (market or limit),
    quantity and a direction.
    """

    def __init__(self, symbol, order_type, quantity, direction):
        """
        Initialised the order type.

        Args:
            symbol (str) - The ticker symbol e.g. 'GOOG'.
            order_type (str) - 'MKT' OR 'LMT' for Market or Limit.
            quantity (int) - Non negative integer for quantity.
            direction (str) - 'BUY' or 'SELL' for long or short. 
        """

        self.type = "ORDER"
        self.symbol = symbol
        self.order_type = order_type
        self.quantity = quantity
        self.direction = direction

    def print_order(self):
        """
        Outputs the value in the OrderEvent
        """
        print(
            f"Order: Symbol={self.symbol}, Type={self.order_type}, Quantity={self.quantity}, Direction={self.direction}"
        )

class FillEvent(Event):
    '''
    Represents the Fill Order, which stores the quantity of an instrument
    actually filled and at what price as well as the commission of the trade from the brokerage. 
    '''

    def __init__(self, timeindex, symbol, exchange, quantity, direction, fill_cost, commission=None):
        '''
        Initialises the FillEvent object.

        If commission is not provided, the Fill object will
        calculate it based on the trade size and Interactive
        Brokers fees.

        Args:
            timeindex - The bar-resolution when the order was filled
            symbol (str) - The instrument which must be filled.
            exchange - The exchange where the order was filled.
            quantity -  The filled quantity
            direction - The direction of fill ('BUY' or 'SELL')
            fill_cost - The holdings valuer in dollars
            commission (optional) - An optional commision sent from IB. 
        '''

        self.type = 'FILL'
        self.timeindex = timeindex
        self.symbol = symbol
        self.exchange = exchange
        self.quantity = quantity
        self.direction = direction
        self.fill_cost = fill_cost

        if commission is None:
            self.commision = self.calculate_ib_commission()-
        else:
            self.commision = commission
        
    def calculate_ib_commission(self):
        '''
        Calculates the fees of trading based on an Interactive
        Brokers fee structure for API, in USD.

        This does not include exchange or ECN fees.

        Based on "US API Directed Orders":
        https://www.interactivebrokers.com/en/index.php?f=commission&p=stocks2
        '''
        full_cost = 1.3
        if self.quantity <= 500:
            full_cost = max(1.3, 0.013 * self.quantity)
        else:
            full_cost = max(1.3, 0.008 * self.quantity)
        full_cost = min(full_cost, 0.5 / 100.0 * self.quantity * self.fill_cost)
        
        return full_cost
