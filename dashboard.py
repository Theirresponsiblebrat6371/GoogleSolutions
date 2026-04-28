from sqlalchemy import func
from sqlalchemy.orm import Session

from config import get_settings
from models import Report, Task, TaskStatus, Volunteer


def get_dashboard_summary(db: Session) -> dict:
    settings = get_settings()
    total_reports = db.query(func.count(Report.id)).scalar() or 0
    open_tasks = db.query(func.count(Task.id)).filter(Task.status != TaskStatus.completed).scalar() or 0
    active_volunteers = db.query(func.count(Volunteer.id)).filter(Volunteer.is_active.is_(True)).scalar() or 0
    urgent_tasks = db.query(func.count(Task.id)).filter(Task.priority_score >= settings.priority_threshold).scalar() or 0
    average_priority = db.query(func.avg(Task.priority_score)).scalar() or 0
    return {
        "total_reports": total_reports,
        "open_tasks": open_tasks,
        "active_volunteers": active_volunteers,
        "urgent_tasks": urgent_tasks,
        "average_priority": round(float(average_priority), 2),
    }
