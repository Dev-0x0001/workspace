export ITERATION_START=$(date +%s)

# Capture initial metrics
python metrics_baseline.py > /tmp/iteration_metrics_${ITERATION_START}.json

# Execute iteration
./run_iteration.sh ${ITERATION_START}

# Collect results
python collect_results.py ${ITERATION_START}