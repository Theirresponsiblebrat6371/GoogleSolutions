from sqlalchemy.orm import Session

from matching import match_task_to_volunteers
from models import Assignment, Task


def run_matching_for_task(db: Session, task: Task) -> list[Assignment]:
    return match_task_to_volunteers(db, task)
