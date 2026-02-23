#!/bin/bash

# Systemd-timers investigation script

# Check if systemd is running
if pgrep -x "systemd" > /dev/null; then
    echo "Systemd is running"
    systemctl --version
    
    # Check timer capabilities
    echo "\nTimer capabilities check:""":
    systemctl list-timers --help | grep -A 5 "TIMER Units"
    
    # User-specific timer check
    echo "\nUser-specific timers:""
    systemctl --user list-timers
    
    # Timer properties example
    echo "\nTimer properties example:""":
    systemctl show --property=AccuracySec,OnCalendar,Unit --value timers.target
else
    echo "Systemd is NOT running"
    echo "This investigation requires systemd as the init system"
fi