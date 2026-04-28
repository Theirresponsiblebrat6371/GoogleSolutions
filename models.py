import enum
from datetime import datetime

from sqlalchemy import Boolean, DateTime, Enum, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base


class ReportCategory(str, enum.Enum):
    food = "food"
    health = "health"
    sanitation = "sanitation"
    shelter = "shelter"
    education = "education"
    logistics = "logistics"
    other = "other"


class ReportStatus(str, enum.Enum):
    new = "new"
    reviewed = "reviewed"
    converted = "converted"


class TaskStatus(str, enum.Enum):
    open = "open"
    matched = "matched"
    in_progress = "in_progress"
    completed = "completed"


class AssignmentStatus(str, enum.Enum):
    pending = "pending"
    notified = "notified"
    accepted = "accepted"
    declined = "declined"
    completed = "completed"


class NGO(Base):
    __tablename__ = "ngos"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    contact_email: Mapped[str] = mapped_column(String(120), nullable=False, unique=True)
    city: Mapped[str] = mapped_column(String(80), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    reports: Mapped[list["Report"]] = relationship(back_populates="ngo")
    tasks: Mapped[list["Task"]] = relationship(back_populates="ngo")


class Volunteer(Base):
    __tablename__ = "volunteers"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    full_name: Mapped[str] = mapped_column(String(120), nullable=False)
    email: Mapped[str] = mapped_column(String(120), nullable=False, unique=True)
    phone: Mapped[str] = mapped_column(String(30), nullable=True)
    city: Mapped[str] = mapped_column(String(80), nullable=False)
    latitude: Mapped[float] = mapped_column(Float, nullable=False)
    longitude: Mapped[float] = mapped_column(Float, nullable=False)
    availability_hours: Mapped[int] = mapped_column(Integer, default=5)
    skill_tags: Mapped[str] = mapped_column(Text, default="")
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    firebase_uid: Mapped[str] = mapped_column(String(128), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    assignments: Mapped[list["Assignment"]] = relationship(back_populates="volunteer")


class Report(Base):
    __tablename__ = "reports"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    ngo_id: Mapped[int] = mapped_column(ForeignKey("ngos.id"), nullable=False)
    title: Mapped[str] = mapped_column(String(160), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    category: Mapped[ReportCategory] = mapped_column(Enum(ReportCategory), default=ReportCategory.other)
    city: Mapped[str] = mapped_column(String(80), nullable=False)
    latitude: Mapped[float] = mapped_column(Float, nullable=False)
    longitude: Mapped[float] = mapped_column(Float, nullable=False)
    people_affected: Mapped[int] = mapped_column(Integer, default=1)
    urgency_hint: Mapped[int] = mapped_column(Integer, default=50)
    resource_type: Mapped[str] = mapped_column(String(80), default="general")
    status: Mapped[ReportStatus] = mapped_column(Enum(ReportStatus), default=ReportStatus.new)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    ngo: Mapped["NGO"] = relationship(back_populates="reports")
    task: Mapped["Task"] = relationship(back_populates="source_report", uselist=False)


class Task(Base):
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    ngo_id: Mapped[int] = mapped_column(ForeignKey("ngos.id"), nullable=False)
    report_id: Mapped[int] = mapped_column(ForeignKey("reports.id"), nullable=False, unique=True)
    title: Mapped[str] = mapped_column(String(160), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    required_volunteers: Mapped[int] = mapped_column(Integer, default=1)
    skill_required: Mapped[str] = mapped_column(String(80), default="general")
    latitude: Mapped[float] = mapped_column(Float, nullable=False)
    longitude: Mapped[float] = mapped_column(Float, nullable=False)
    city: Mapped[str] = mapped_column(String(80), nullable=False)
    priority_score: Mapped[int] = mapped_column(Integer, default=0)
    status: Mapped[TaskStatus] = mapped_column(Enum(TaskStatus), default=TaskStatus.open)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    ngo: Mapped["NGO"] = relationship(back_populates="tasks")
    source_report: Mapped["Report"] = relationship(back_populates="task")
    assignments: Mapped[list["Assignment"]] = relationship(back_populates="task")


class Assignment(Base):
    __tablename__ = "assignments"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    task_id: Mapped[int] = mapped_column(ForeignKey("tasks.id"), nullable=False)
    volunteer_id: Mapped[int] = mapped_column(ForeignKey("volunteers.id"), nullable=False)
    distance_km: Mapped[float] = mapped_column(Float, default=0.0)
    match_score: Mapped[int] = mapped_column(Integer, default=0)
    status: Mapped[AssignmentStatus] = mapped_column(Enum(AssignmentStatus), default=AssignmentStatus.pending)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    task: Mapped["Task"] = relationship(back_populates="assignments")
    volunteer: Mapped["Volunteer"] = relationship(back_populates="assignments")
