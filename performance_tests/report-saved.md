VERTICA REPORT:
{
  "test_read": {
    "operation": "select distinct user_id from test where ts > 2400;",
    "iterations": 50,
    "avg_seconds": 0.6887599999969826
  },
  "test_read_mp": {
    "operation": "select distinct user_id from test where ts > 2400;",
    "cores": 4,
    "iterations": 50,
    "avg_seconds": 0.710470000001369
  },
  "test_write": {
    "rec_count": 20000,
    "iterations": 50,
    "avg_seconds": 0.5690799999982119
  },
  "test_write_mp": {
    "rec_count": 20000,
    "cores": 4,
    "iterations": 50,
    "avg_seconds": 0.6287550000019837
  },
  "test_mixed_mp": {
    "read_operation": "select distinct user_id from test where ts > 2400;",
    "rec_count": 20000,
    "cores": 4,
    "iterations": 50,
    "avg_read_seconds": 1.0459499999973922,
    "avg_write_seconds": 0.619069999998901
  }
}
CLICKHOUSE REPORT:
{
  "test_read": {
    "operation": "select distinct user_id from docker.test where ts > 2400;",
    "iterations": 50,
    "avg_seconds": 0.1384400000004098
  },
  "test_read_mp": {
    "operation": "select distinct user_id from docker.test where ts > 2400;",
    "cores": 4,
    "iterations": 50,
    "avg_seconds": 0.16047000000136905
  },
  "test_write": {
    "rec_count": 20000,
    "iterations": 50,
    "avg_seconds": 0.0871999999973923
  },
  "test_write_mp": {
    "rec_count": 20000,
    "cores": 4,
    "iterations": 50,
    "avg_seconds": 0.09367499999934806
  },
  "test_mixed_mp": {
    "read_operation": "select distinct user_id from docker.test where ts > 2400;",
    "rec_count": 20000,
    "cores": 4,
    "iterations": 50,
    "avg_read_seconds": 0.20264000000199303,
    "avg_write_seconds": 0.10562999999849126
  }
}
