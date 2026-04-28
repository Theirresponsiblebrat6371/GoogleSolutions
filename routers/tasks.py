from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from models import Task
from schemas import AssignmentRead, MatchRequest, TaskRead
from services.notification_service import notify_assignment
from services.volunteer_matcher import run_matching_for_task


router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.get("/", response_model=list[TaskRead])
def list_tasks(db: Session = Depends(get_db)):
    return db.query(Task).order_by(Task.priority_score.desc(), Task.created_at.desc()).all()


@router.post("/match", response_model=list[AssignmentRead])
def match_volunteers(payload: MatchRequest, db: Session = Depends(get_db)):
    task = db.query(Task).filter(Task.id == payload.task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    assignments = run_matching_for_task(db, task)
    for assignment in assignments:
        notify_assignment(db, assignment)
    return assignments
