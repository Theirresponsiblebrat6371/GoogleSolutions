from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from dashboard import get_dashboard_summary
from database import get_db
from schemas import DashboardSummary


router = APIRouter(prefix="/dashboard", tags=["dashboard"])


@router.get("/summary", response_model=DashboardSummary)
def dashboard_summary(db: Session = Depends(get_db)):
    return get_dashboard_summary(db)
