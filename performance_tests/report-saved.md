VERTICA REPORT:
{
  "test_read": {
    "operation": "select distinct user_id from test where ts > 2400;",
    "iterations": 50,
    "avg_seconds": 0.6853000000026077
  },
  "test_read_mp": {
    "operation": "select distinct user_id from test where ts > 2400;",
    "cores": 4,
    "iterations": 50,
    "avg_seconds": 0.7294599999999628
  },
  "test_write": {
    "rec_count": 20000,
    "iterations": 50,
    "avg_seconds": 0.5693600000021979
  },
  "test_write_mp": {
    "rec_count": 20000,
    "cores": 4,
    "iterations": 50,
    "avg_seconds": 0.6112549999984913
  },
  "test_mixed_mp": {
    "read_operation": "select distinct user_id from test where ts > 2400;",
    "rec_count": 20000,
    "cores": 4,
    "iterations": 50,
    "avg_read_seconds": 1.0504600000008941,
    "avg_write_seconds": 0.6207899999967776
  }
}
CLICKHOUSE REPORT:
{
  "test_read": {
    "operation": "select distinct user_id from docker.test where ts > 2400;",
    "iterations": 50,
    "avg_seconds": 0.13623999999836087
  },
  "test_read_mp": {
    "operation": "select distinct user_id from docker.test where ts > 2400;",
    "cores": 4,
    "iterations": 50,
    "avg_seconds": 0.1649250000016764
  },
  "test_write": {
    "rec_count": 20000,
    "iterations": 50,
    "avg_seconds": 0.08623999999836088
  },
  "test_write_mp": {
    "rec_count": 20000,
    "cores": 4,
    "iterations": 50,
    "avg_seconds": 0.08898000000044703
  },
  "test_mixed_mp": {
    "read_operation": "select distinct user_id from docker.test where ts > 2400;",
    "rec_count": 20000,
    "cores": 4,
    "iterations": 50,
    "avg_read_seconds": 0.18843999999575317,
    "avg_write_seconds": 0.09687999999849126
  }
}
