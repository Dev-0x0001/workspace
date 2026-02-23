import psycopg2
import json
from datetime import datetime

# Database connection parameters
DB_PARAMS = {
    'host': 'localhost',
    'port': '5432',
    'database': 'performance_db',
    'user': 'perf_monitor',
    'password': 'secure_password'
}

class DatabaseMetricsCollector:
    """Collects PostgreSQL database performance metrics"""
    
    def __init__(self):
        self.conn = None
        self.metrics = []
        
    def connect(self):
        """Establish database connection"""
        try:
            self.conn = psycopg2.connect(**DB_PARAMS)
            self.conn.autocommit = True
            print("Connection established")
            return True
        except psycopg2.Error as e:
            print(f"Connection failed: {e}")
            return False

    def collect_metrics(self):
        """Collect comprehensive performance metrics"""
        if not self.conn:
            self.connect()

        try:
            cur = self.conn.cursor()
            
            # Collect query statistics
            cur.execute("""
                SELECT
                    query_id,
                    query_text,
                    round(total_rows::numeric, 2) AS total_rows,
                    round(total_logical_reads::numeric, 2) AS total_logical_reads,
                    round(total_worker_time::numeric, 2) AS total_worker_time,
                    round(total_elapsed_time::numeric, 2) AS total_elapsed_time
                FROM
                    (SELECT
                         query_id,
                         query_text,
                         SUM(rows) AS total_rows,
                         SUM(logical_reads) AS total_logical_reads,
                         SUM(worker_time) AS total_worker_time,
                         SUM(elapsed_time) AS total_elapsed_time
                     FROM
                         sys.dm_exec_query_stats
                     CROSS APPLY
                         (SELECT TOP 1 query_text = t.text
                          FROM sys.dm_exec_sql_text(sql_handle) AS t)
                     GROUP BY
                         query_id, query_text) AS stats
            """)
            
            query_metrics = cur.fetchall()
            self.metrics.extend([
                {'type': 'query', 'timestamp': datetime.now(), **row}
                for row in query_metrics
            ])

            # Collect lock contention metrics
            cur.execute("""
                SELECT
                    resource_type,
                    resource_database_id,
                    resource_object_id,
                    resource_description,
                    request_mode,
                    request_type,
                    request_waiting,
                    request_duration_seconds
                FROM
                    sys.dm_tran_locks
            """)
            
            lock_metrics = cur.fetchall()
            self.metrics.extend([
                {'type': 'lock', 'timestamp': datetime.now(), **row}
                for row in lock_metrics
            ])

            # Collect index usage statistics
            cur.execute("""
                SELECT
                    object_id,
                    index_id,
                    name AS index_name,
                    user_seeks,
                    user_scans,
                    user_updates,
                    last_user_update
                FROM
                    sys.dm_db_index_usage_stats
            """)
            
            index_metrics = cur.fetchall()
            self.metrics.extend([
                {'type': 'index', 'timestamp': datetime.now(), **row}
                for row in index_metrics
            ])

            print(f"Collected {len(self.metrics)} metrics")
            return True
        except psycopg2.Error as e:
            print(f"Metrics collection failed: {e}")
            return False

    def save_metrics(self, filename='metrics.json'):
        """Save metrics to file"""
        if self.metrics:
            with open(filename, 'w') as f:
                json.dump(self.metrics, f, indent=4)
            print(f"Metrics saved to {filename}")
        else:
            print("No metrics to save")

    def __del__(self):
        """Clean up database connection"""
        if self.conn:
            self.conn.close()
            print("Connection closed")