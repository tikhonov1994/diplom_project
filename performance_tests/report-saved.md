VERTICA REPORT:
{
  "test_read": {
    "operation": "select distinct state from test where longitude > latitude;",
    "iterations": 100,
    "avg_seconds": 0.09609999999869615
  },
  "test_read_mp": {
    "operation": "select distinct state from test where longitude > latitude;",
    "cores": 8,
    "iterations": 100,
    "avg_seconds": 0.16327875000046332
  },
  "test_write": {
    "chunk_file": "./test_data/Eartquakes-1990-2023.chunk.csv",
    "iterations": 100,
    "avg_seconds": 0.009219999997876585
  },
  "test_write_mp": {
    "chunk_file": "./test_data/Eartquakes-1990-2023.chunk.csv",
    "cores": 8,
    "iterations": 100,
    "avg_seconds": 0.030781250000291038
  },
  "test_mixed_mp": {
    "read_operation": "select distinct state from test where longitude > latitude;",
    "write_chunk_file": "./test_data/Eartquakes-1990-2023.chunk.csv",
    "cores": 8,
    "iterations": 100,
    "avg_read_seconds": 0.11910249999957159,
    "avg_write_seconds": 0.02781499999924563
  }
}

CLICKHOUSE REPORT:
{
  "test_read": {
    "operation": "select distinct state from docker.test where longitude > latitude;",
    "iterations": 100,
    "avg_seconds": 0.04015000000130385
  },
  "test_read_mp": {
    "operation": "select distinct state from docker.test where longitude > latitude;",
    "cores": 8,
    "iterations": 100,
    "avg_seconds": 0.1268737500003772
  },
  "test_write": {
    "chunk_file": "./test_data/Eartquakes-1990-2023.chunk.csv",
    "iterations": 100,
    "avg_seconds": 0.06358999999938533
  },
  "test_write_mp": {
    "chunk_file": "./test_data/Eartquakes-1990-2023.chunk.csv",
    "cores": 8,
    "iterations": 100,
    "avg_seconds": 0.12251750000024914
  },
  "test_mixed_mp": {
    "read_operation": "select distinct state from docker.test where longitude > latitude;",
    "write_chunk_file": "./test_data/Eartquakes-1990-2023.chunk.csv",
    "cores": 8,
    "iterations": 100,
    "avg_read_seconds": 0.15894250000070315,
    "avg_write_seconds": 0.1386725000006845
  }
}
