CATEGORY_WEIGHTS = {
    "health": 30,
    "food": 24,
    "sanitation": 20,
    "shelter": 18,
    "logistics": 14,
    "education": 10,
    "other": 8,
}


def score_report(report) -> int:
    category = getattr(report.category, "value", report.category)
    people_component = min(report.people_affected * 2, 30)
    urgency_component = min(report.urgency_hint, 35)
    category_component = CATEGORY_WEIGHTS.get(str(category).lower(), 8)
    resource_bonus = 10 if report.resource_type.lower() in {"medical", "food", "sanitation"} else 4
    score = people_component + urgency_component + category_component + resource_bonus
    return min(score, 100)
