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
