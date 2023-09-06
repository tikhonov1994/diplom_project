VERTICA REPORT:
{
  "test_read": {
    "operation": "select distinct user_id from test where ts > 2400;",
    "iterations": 20,
    "avg_seconds": 0.00625
  },
  "test_read_mp": {
    "operation": "select distinct user_id from test where ts > 2400;",
    "cores": 4,
    "iterations": 20,
    "avg_seconds": 0.009349999998812565
  },
  "test_write": {
    "rec_count": 30000,
    "iterations": 20,
    "avg_seconds": 0.83125
  },
  "test_write_mp": {
    "rec_count": 30000,
    "cores": 4,
    "iterations": 20,
    "avg_seconds": 0.9297000000020489
  },
  "test_mixed_mp": {
    "read_operation": "select distinct user_id from test where ts > 2400;",
    "rec_count": 30000,
    "cores": 4,
    "iterations": 20,
    "avg_read_seconds": 0.2590000000025611,
    "avg_write_seconds": 0.8738249999994878
  }
}
CLICKHOUSE REPORT:
{
  "test_read": {
    "operation": "select distinct user_id from docker.test where ts > 2400;",
    "iterations": 20,
    "avg_seconds": 0.0023000000044703485
  },
  "test_read_mp": {
    "operation": "select distinct user_id from docker.test where ts > 2400;",
    "cores": 4,
    "iterations": 20,
    "avg_seconds": 0.002350000001024455
  },
  "test_write": {
    "rec_count": 30000,
    "iterations": 20,
    "avg_seconds": 0.11330000000307336
  },
  "test_write_mp": {
    "rec_count": 30000,
    "cores": 4,
    "iterations": 20,
    "avg_seconds": 0.12499999999708962
  },
  "test_mixed_mp": {
    "read_operation": "select distinct user_id from docker.test where ts > 2400;",
    "rec_count": 30000,
    "cores": 4,
    "iterations": 20,
    "avg_read_seconds": 0.04102499999571592,
    "avg_write_seconds": 0.10782499999622815
  }
}
