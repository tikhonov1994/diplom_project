POSTGRES REPORT:
{
  "test_read": {
    "operation": "SELECT * FROM reviews LEFT JOIN likes ON reviews.review_id = likes.entity_id where reviews.user_id = %s;",
    "iterations": 5,
    "avg_seconds": 0.27023190859999885
  },
  "test_read_avg": {
    "operation": "SELECT AVG(value) FROM likes WHERE entity_id = %s GROUP BY entity_id;",
    "iterations": 5,
    "avg_seconds": 0.032384649999949035
  },
  "test_count_likes": {
    "operation": "SELECT COUNT(*) FROM likes where likes.user_id = %s and value = 10;",
    "iterations": 5,
    "avg_seconds": 0.0005776251999122905
  },
  "test_read_mp": {
    "operation": "SELECT * FROM reviews LEFT JOIN likes ON reviews.review_id = likes.entity_id where reviews.user_id = %s;",
    "cores": 4,
    "iterations": 5,
    "avg_seconds": 0.355798933300025
  },
  "test_write": {
    "rec_count": 10000,
    "iterations": 5,
    "avg_seconds": 0.45317647519996174
  },
  "test_write_mp": {
    "rec_count": 10000,
    "cores": 4,
    "iterations": 5,
    "avg_seconds": 0.6068862626499821
  },
  "test_mixed_mp": {
    "read_operation": "SELECT * FROM reviews LEFT JOIN likes ON reviews.review_id = likes.entity_id where reviews.user_id = %s;",
    "rec_count": 10000,
    "cores": 4,
    "iterations": 5,
    "avg_read_seconds": 0.3834487831999013,
    "avg_write_seconds": 0.564142587399965
  }
}
MONGO REPORT:
{
  "test_read": {
    "operation": "SELECT * FROM reviews where reviews.user_id = %s;",
    "iterations": 5,
    "avg_seconds": 0.0003274997999596962
  },
  "test_read_avg": {
    "operation": "SELECT AVG(value) FROM movieLikes WHERE entity_id = %s GROUP BY entity_id;",
    "iterations": 5,
    "avg_seconds": 0.0049824833999537075
  },
  "test_count_likes": {
    "operation": "SELECT COUNT(*) FROM likes where likes.user_id = %s and value = 10;",
    "iterations": 5,
    "avg_seconds": 0.00465152480001052
  },
  "test_read_mp": {
    "operation": "SELECT * FROM reviews where reviews.user_id = %s;",
    "cores": 4,
    "iterations": 5,
    "avg_seconds": 4.665629998044097e-05
  },
  "test_write": {
    "rec_count": 10000,
    "iterations": 5,
    "avg_seconds": 0.4433662751999691
  },
  "test_write_mp": {
    "rec_count": 10000,
    "cores": 4,
    "iterations": 5,
    "avg_seconds": 1.4714869915999882
  },
  "test_mixed_mp": {
    "read_operation": "SELECT * FROM reviews where reviews.user_id = %s;",
    "rec_count": 10000,
    "cores": 4,
    "iterations": 5,
    "avg_read_seconds": 0.00010001670002566244,
    "avg_write_seconds": 0.9586654332999842
  }
}
