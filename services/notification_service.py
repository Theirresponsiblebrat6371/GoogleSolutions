from sqlalchemy.orm import Session

from models import Assignment, Volunteer
from notifications import send_push_notification


def notify_assignment(db: Session, assignment: Assignment) -> dict:
    volunteer = db.query(Volunteer).filter(Volunteer.id == assignment.volunteer_id).first()
    target = volunteer.firebase_uid if volunteer and volunteer.firebase_uid else volunteer.email
    return send_push_notification(
        target=target,
        title="New volunteer task assigned",
        body=f"You have been matched to task #{assignment.task_id}. Please review it in the volunteer app.",
    )
