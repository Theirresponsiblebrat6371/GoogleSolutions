from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from database import get_db
from models import NGO, Report, ReportStatus, Task
from schemas import ReportCreate, ReportRead, TaskRead
from services.priority_engine import calculate_priority


router = APIRouter(prefix="/reports", tags=["reports"])


@router.get("/", response_model=list[ReportRead])
def list_reports(db: Session = Depends(get_db)):
    return db.query(Report).order_by(Report.created_at.desc()).all()


@router.post("/", response_model=TaskRead, status_code=status.HTTP_201_CREATED)
def create_report(payload: ReportCreate, db: Session = Depends(get_db)):
    ngo = db.query(NGO).filter(NGO.id == payload.ngo_id).first()
    if not ngo:
        raise HTTPException(status_code=404, detail="NGO not found")

    report = Report(**payload.model_dump())
    db.add(report)
    db.flush()

    priority = calculate_priority(report)
    task = Task(
        ngo_id=report.ngo_id,
        report_id=report.id,
        title=report.title,
        description=report.description,
        required_volunteers=max(1, min(10, report.people_affected // 10 or 1)),
        skill_required=report.resource_type,
        latitude=report.latitude,
        longitude=report.longitude,
        city=report.city,
        priority_score=priority,
    )
    report.status = ReportStatus.converted
    db.add(task)
    db.commit()
    db.refresh(task)
    return task
