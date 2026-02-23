SELECT
  queries.query_id,
  queries.query_text,
  execution_stats.total_rows,
  execution_stats.total_logical_reads,
  execution_stats.total_worker_time,
  execution_stats.total_elapsed_time,
  waits.wait_type,
  waits.wait_time_ms,
  index_usage.object_id,
  index_usage.index_id,
  index_usage.user_seeks,
  index_usage.user_scans,
  index_usage.user_updates
FROM
  (SELECT DISTINCT query_id, query_text FROM sys.dm_exec_query_stats AS stats
  CROSS APPLY (SELECT TOP 1 query_text = t.text FROM sys.dm_exec_sql_text(stats.sql_handle) AS t) AS t)
  AS queries
LEFT JOIN sys.dm_exec_query_stats AS execution_stats ON queries.query_id = execution_stats.query_id
LEFT JOIN sys.dm_exec_requests AS waits ON queries.query_id = waits.query_id
LEFT JOIN sys.dm_db_index_usage_stats AS index_usage ON queries.object_id = index_usage.object_id