export MEASUREMENT_TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S %Z')
export UPTIME_RAW=$(uptime)
export LOAD_AVERAGES=$(uptime | awk '{print $5, $6, $7}' | tr ' ' ',')

export MEMORY_TOTAL=$(free -m | grep Mem | awk '{print $2}')
export MEMORY_FREE=$(free -m | grep Mem | awk '{print $3}')
export MEMORY_USED=$(free -m | grep Mem | awk '{print $3}')
export MEMORY_AVAILABLE=$(free -m | grep Mem | awk '{print $7}')

export SWAP_TOTAL=$(free -m | grep Swap | awk '{print $2}')
export SWAP_FREE=$(free -m | grep Swap | awk '{print $3}')
export SWAP_USED=$(free -m | grep Swap | awk '{print $4}')

export FILESYSTEM_DATA=$(df -h | grep '/dev' | awk '{print $1, $2, $3, $4, $5, $6}')

export TOP_SNAPSHOT=$(top -b -n 1 | head -n 20)
