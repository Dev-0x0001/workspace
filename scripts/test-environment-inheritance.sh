#!/bin/bash

# Shell Startup File Investigation
#
# This script tests how environment variables are inherited
# and identifies potential security restrictions.

#=====================================================
# Configuration
#=====================================================

# Test environment variables
export TEST_VAR="secure_value"
export PATH_MODIFICATION="${PATH}:/tmp/test-path"

#=====================================================
# Startup File Simulation
#=====================================================

# Common shell startup files in order of precedence
STARTUP_FILES=(
    "/etc/profile"
    "~/.bash_profile"
    "~/.bashrc"
    "~/.bash_login"
    "~/.profile"
    "/etc/bash.bashrc"
)

#=====================================================
# Environment Tracing Functions
#=====================================================

# Capture environment state
capture_env() {
    echo "--- Capture at: $(date) ---"
    env | sort | tee "env-",$(date +%Y%m%d-%H%M%S),.txt
}

# Track variable changes
track_variable() {
    local var_name=$1
    local capture_count=0
    
    echo "Tracking variable: ${var_name}" |
}

#=====================================================
# Test Scenarios
#=====================================================

# Test 1: Basic inheritance
test_basic_inheritance() {
    echo "=== Test 1: Basic Environment Inheritance ==="
    
    # Create child shell
    ( 
        capture_env
        
        # Check for inherited variables
        echo "TEST_VAR = "${TEST_VAR}""
        echo "PATH = "${PATH}""
        
        # Modify variables
        export TEST_VAR="modified_value"
        export PATH="${PATH}:/tmp/test-path-modified"
        
        capture_env
    )
}

# Test 2: Restricted environments
test_restricted_environments() {
    echo "=== Test 2: Restricted Environment Scenarios ==="
    
    # Test with non-interactive shell
    echo "-- Non-interactive shell --"
    (exec env -i TEST_VAR="secure_value" bash -c 'capture_env && echo "TEST_VAR = "${TEST_VAR}""')
    
    # Test with limited environment
    echo "-- Limited environment --"
    (exec env -i PATH="/usr/bin:/bin" bash -c 'capture_env && which ls')
}

# Test 3: Startup file impact
test_startup_file_impact() {
    echo "=== Test 3: Startup File Effects ==="
    
    for file in "${STARTUP_FILES[@]}"; do
        if [ -f "${file}" ]; then
            echo "-- Testing: ${file} --"
            (source "${file}" && capture_env)
        else
            echo "Skipping missing file: ${file}" 
        fi
    done
}

#=====================================================
# Main Execution
#=====================================================

echo "=== Environment Inheritance Investigation ==="

capture_env

test_basic_inheritance
test_restricted_environments
test_startup_file_impact

echo "=== Investigation Complete ==="
