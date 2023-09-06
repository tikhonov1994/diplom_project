import json

from test_base import TestBase
from clickhouse_tests import ClickhouseTests
from vertica_tests import VerticaTests

_PROCESSES = 4
_ITERATIONS = 50
_REC_WRITE_COUNT = 20000
_PRE_FILLED_REC_COUNT = 1000000


def collect_report(test_provider: TestBase) -> dict[str, any]:
    report = {}

    # Test Read
    report |= test_provider.test_read(_ITERATIONS)
    report |= test_provider.test_read_mp(_PROCESSES, _ITERATIONS)

    # Test Write
    report |= test_provider.test_write(_REC_WRITE_COUNT, _ITERATIONS)
    report |= test_provider.test_write_mp(_REC_WRITE_COUNT, _PROCESSES, _ITERATIONS)

    # Test Mixed
    report |= test_provider.test_mixed_mp(_REC_WRITE_COUNT, _PROCESSES, _ITERATIONS)

    return report


if __name__ == '__main__':
    report_lines = []

    vertica_tests = VerticaTests(pre_filled_rec_count=_PRE_FILLED_REC_COUNT)
    vertica_report = collect_report(vertica_tests)
    report_lines.append('VERTICA REPORT:\n')
    report_lines.append(json.dumps(vertica_report, indent=2))
    report_lines.append('\n')

    clickhouse_tests = ClickhouseTests(pre_filled_rec_count=_PRE_FILLED_REC_COUNT)
    clickhouse_report = collect_report(clickhouse_tests)
    report_lines.append('CLICKHOUSE REPORT:\n')
    report_lines.append(json.dumps(clickhouse_report, indent=2))
    report_lines.append('\n')

    with open('report.md', 'w') as report_file:
        report_file.writelines(report_lines)
