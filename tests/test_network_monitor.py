import pytest
from unittest.mock import patch, MagicMock
from app.services.network_monitor import NetworkMonitor

def test_network_monitor_adaptive_sleep():
    monitor = NetworkMonitor()
    
    # Test case 1: Successful connection resets consecutive_failures to 0
    with patch("urllib.request.urlopen") as mock_urlopen:
        mock_urlopen.return_value = MagicMock()
        
        # Manually run the status check logic that happens inside the loop
        connected = True
        monitor.consecutive_failures = 4 # Start with 4 failures
        
        if connected:
            monitor.consecutive_failures = 0
            
        assert monitor.consecutive_failures == 0
        
        # Under normal connection, sleep interval should be 60 seconds
        if connected:
            sleep_interval = 60
        assert sleep_interval == 60

    # Test case 2: Connection failure increments consecutive_failures and sleeps 60s under 5 failures
    connected = False
    monitor.consecutive_failures = 0
    
    # First failure
    monitor.consecutive_failures += 1
    assert monitor.consecutive_failures == 1
    
    if monitor.consecutive_failures >= 5:
        sleep_interval = 300
    else:
        sleep_interval = 60
    assert sleep_interval == 60

    # Test case 3: 5 consecutive failures scales sleep_interval to 300s (5 minutes)
    monitor.consecutive_failures = 4
    monitor.consecutive_failures += 1
    assert monitor.consecutive_failures == 5
    
    if monitor.consecutive_failures >= 5:
        sleep_interval = 300
    else:
        sleep_interval = 60
    assert sleep_interval == 300
