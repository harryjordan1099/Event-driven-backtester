from backtester.event import MarketEvent, SignalEvent, OrderEvent, FillEvent
from datetime import datetime

def test_market_event_initialization():
    # Test initialization of MarketEvent object
    market_event = MarketEvent()
    
    assert market_event.type == "MARKET", "Type attribute not initialized correctly"

def test_signal_event_initialization():
    # Test initialization of SignalEvent object
    symbol = "AAPL"
    timestamp = datetime.now()
    signal_type = "LONG"
    
    signal_event = SignalEvent(symbol, timestamp, signal_type)
    
    assert signal_event.type == "SIGNAL", "Type attribute not initialized correctly"
    assert signal_event.symbol == symbol, "Symbol attribute not initialized correctly"
    assert signal_event.datetime == timestamp, "Datetime attribute not initialized correctly"
    assert signal_event.signal_type == signal_type, "Signal type attribute not initialized correctly"

def test_order_event_print_order(capsys):
    # Create an instance of OrderEvent with sample values
    order_event = OrderEvent("GOOG", "MKT", 100, "BUY")
    
    # Call the print_order method
    order_event.print_order()
    
    # Capture the printed output
    captured = capsys.readouterr()
    
    # Check if the printed output matches the expected format
    expected_output = "Order: Symbol=GOOG, Type=MKT, Quantity=100, Direction=BUY\n"
    assert captured.out == expected_output

def test_fill_event_initialization():
    # Test initialization of FillEvent object
    fill_event = FillEvent(timeindex=123, symbol="AAPL", exchange="NYSE", quantity=100, direction="BUY", fill_cost=1000)
    
    assert fill_event.type == "FILL", "event Type attribute not initialized correctly"
    assert fill_event.timeindex == 123, "Timeindex attribute not initialized correctly"
    assert fill_event.symbol == "AAPL", "Symbol attribute not initialized correctly"
    assert fill_event.exchange == "NYSE", "Exchange attribute not initialized correctly"
    assert fill_event.quantity == 100, "Quantity attribute not initialized correctly"
    assert fill_event.direction == "BUY", "Direction attribute not initialized correctly"
    assert fill_event.fill_cost == 1000, "Fill cost attribute not initialized correctly"

def test_fill_event_commission_calculation_below_500():
    # Test commission calculation for a small quantity
    fill_event_small = FillEvent(timeindex=123, symbol="AAPL", exchange="NYSE", quantity=100, direction="BUY", fill_cost=1000)
    assert fill_event_small.commision == max(1.3, 0.013 * fill_event_small.quantity)

def test_fill_event_commission_calculation_above_500():
    # Test commission calculation for a large quantity
    fill_event_large = FillEvent(timeindex=123, symbol="AAPL", exchange="NYSE", quantity=1000, direction="BUY", fill_cost=1000)
    assert fill_event_large.commision == max(1.3, 0.008 * fill_event_large.quantity)


 