from models import Report
from prioritization import score_report


def calculate_priority(report: Report) -> int:
    return score_report(report)
