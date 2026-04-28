from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from database import get_db
from models import Volunteer
from schemas import VolunteerCreate, VolunteerRead


router = APIRouter(prefix="/volunteers", tags=["volunteers"])


@router.get("/", response_model=list[VolunteerRead])
def list_volunteers(db: Session = Depends(get_db)):
    return db.query(Volunteer).order_by(Volunteer.created_at.desc()).all()


@router.post("/", response_model=VolunteerRead, status_code=status.HTTP_201_CREATED)
def create_volunteer(payload: VolunteerCreate, db: Session = Depends(get_db)):
    volunteer = Volunteer(**payload.model_dump())
    db.add(volunteer)
    db.commit()
    db.refresh(volunteer)
    return volunteer
