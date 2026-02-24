export MEASUREMENT_ID=$(date +%s)

echo "=== Baseline Measurement ==="
echo "Timestamp: $MEASUREMENT_TIMESTAMP"
echo "Uptime: $UPTIME_RAW"
echo "Load Averages: $LOAD_AVERAGES"

echo "\nMemory Status:"
echo "  Total: ${MEMORY_TOTAL}MiB"
echo "  Free: ${MEMORY_FREE}MiB"
echo "  Used: ${MEMORY_USED}MiB"
echo "  Available: ${MEMORY_AVAILABLE}MiB"

echo "\nSwap Status:"
echo "  Total: ${SWAP_TOTAL}MiB"
echo "  Free: ${SWAP_FREE}MiB"
echo "  Used: ${SWAP_USED}MiB"

echo "\nFilesystem Status:"
echo "  ${FILESYSTEM_DATA}" 

echo "\nTop Snapshot (first 20 lines):"
echo "  ${TOP_SNAPSHOT}"