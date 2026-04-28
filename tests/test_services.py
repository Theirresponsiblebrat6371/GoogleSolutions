from types import SimpleNamespace

from matching import compute_match_score
from prioritization import score_report


def test_score_report_caps_at_100():
    report = SimpleNamespace(
        people_affected=100,
        urgency_hint=95,
        category="health",
        resource_type="medical",
    )
    assert score_report(report) == 100


def test_match_score_within_radius_is_positive():
    task = SimpleNamespace(
        latitude=22.8055,
        longitude=86.2060,
        skill_required="food",
        priority_score=90,
    )
    volunteer = SimpleNamespace(
        latitude=22.8046,
        longitude=86.2029,
        skill_tags="food,logistics",
        availability_hours=6,
        is_active=True,
    )
    score, distance = compute_match_score(task, volunteer, 10)
    assert score > 0
    assert distance < 10
