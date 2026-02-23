SELECT
  query_text.query_text,
  execution_stats.total_rows,
  execution_stats.total_execution_time,
  execution_stats.total_wait_time,
  index_usage.object_id,
  index_usage.index_id,
  index_usage.user_seeks,
  index_usage.user_scans,
  lock_stats.lock_wait_count,
  lock_stats.lock_wait_resource,
  lock_stats.lock_wait_avg_duration
FROM
  (SELECT *
   FROM sys.dm_exec_query_stats
   CROSS APPLY sys.dm_exec_sql_text(sql_handle)) AS query_text
CROSS APPLY (
  SELECT SUM(rows) AS total_rows,
         SUM(total_worker_time) / 1000.0 AS total_execution_time,
         SUM(total_wait_time) / 1000.0 AS total_wait_time
  FROM sys.dm_exec_query_stats
  WHERE query_text.sql_handle = sys.dm_exec_query_stats.sql_handle
) AS execution_stats
LEFT JOIN (
  SELECT object_id, index_id,
         SUM(user_seeks) AS user_seeks,
         SUM(user_scans) AS user_scans
  FROM sys.dm_db_index_usage_stats
  GROUP BY object_id, index_id
) AS index_usage ON query_text.objectid = index_usage.object_id
LEFT JOIN (
  SELECT resource_type, object_id, index_id, partition_number,
         SUM(wait_count) AS lock_wait_count,
         SUM(wait_time_ms) AS lock_wait_resource,
         SUM(wait_time_ms) / SUM(wait_count) AS lock_wait_avg_duration
  FROM sys.dm_os_wait_stats
  WHERE resource_type = 'OBJECT'
  GROUP BY resource_type, object_id, index_id, partition_number
) AS lock_stats ON query_text.objectid = lock_stats.object_id;
