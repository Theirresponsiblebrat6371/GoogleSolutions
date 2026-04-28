from sqlalchemy.orm import Session

from config import get_settings
from services.geolocation import distance_km


def compute_match_score(task, volunteer, max_radius_km: float) -> tuple[int, float]:
    distance = distance_km(task.latitude, task.longitude, volunteer.latitude, volunteer.longitude)
    if distance > max_radius_km or not volunteer.is_active:
        return 0, distance

    skill_match = 25 if task.skill_required.lower() in volunteer.skill_tags.lower() else 10
    availability_score = min(volunteer.availability_hours * 5, 25)
    distance_score = max(0, int((1 - (distance / max_radius_km)) * 30))
    score = skill_match + availability_score + distance_score + min(task.priority_score // 5, 20)
    return min(score, 100), distance


def match_task_to_volunteers(db: Session, task) -> list:
    from models import Assignment, AssignmentStatus, TaskStatus, Volunteer

    settings = get_settings()
    volunteers = db.query(Volunteer).filter(Volunteer.is_active.is_(True)).all()
    ranked: list[tuple[int, float, Volunteer]] = []

    for volunteer in volunteers:
        score, distance = compute_match_score(task, volunteer, settings.match_radius_km)
        if score > 0:
            ranked.append((score, distance, volunteer))

    ranked.sort(key=lambda item: (-item[0], item[1]))
    selected = ranked[: task.required_volunteers]
    assignments: list[Assignment] = []

    for score, distance, volunteer in selected:
        assignment = Assignment(
            task_id=task.id,
            volunteer_id=volunteer.id,
            distance_km=round(distance, 2),
            match_score=score,
            status=AssignmentStatus.pending,
        )
        db.add(assignment)
        assignments.append(assignment)

    if assignments:
        task.status = TaskStatus.matched

    db.commit()
    for assignment in assignments:
        db.refresh(assignment)
    return assignments
