import json

from test_base import TestBase
from mongo_tests import MongoTests
from postgres_tests import PostgresTests

_PROCESSES = 4
_ITERATIONS = 5
_REC_WRITE_COUNT = 10000
_PRE_FILLED_REC_COUNT = 1000000


def collect_report(test_provider: TestBase) -> dict[str, any]:
    report = {}

    # Test Read
    report |= test_provider.test_read(_ITERATIONS)
    report |= test_provider.test_read_avg_likes(_ITERATIONS)
    report |= test_provider.test_count_likes(_ITERATIONS)
    report |= test_provider.test_read_mp(_PROCESSES, _ITERATIONS)

    # Test Write
    report |= test_provider.test_write(_REC_WRITE_COUNT, _ITERATIONS)
    report |= test_provider.test_write_mp(_REC_WRITE_COUNT, _PROCESSES, _ITERATIONS)

    # Test Mixed
    report |= test_provider.test_mixed_mp(_REC_WRITE_COUNT, _PROCESSES, _ITERATIONS)

    return report


if __name__ == '__main__':
    report_lines = []

    mongo_tests = MongoTests(pre_filled_rec_count=_PRE_FILLED_REC_COUNT)
    mongo_report = collect_report(mongo_tests)
    report_lines.append('MONGO REPORT:\n')
    report_lines.append(json.dumps(mongo_report, indent=2))
    report_lines.append('\n')

    postgres_tests = PostgresTests(pre_filled_rec_count=_PRE_FILLED_REC_COUNT)
    postgres_report = collect_report(postgres_tests)
    report_lines.append('POSTGRES REPORT:\n')
    report_lines.append(json.dumps(postgres_report, indent=2))
    report_lines.append('\n')

    print('generating report...')
    with open('report.md', 'w') as report_file:
        report_file.writelines(report_lines)
