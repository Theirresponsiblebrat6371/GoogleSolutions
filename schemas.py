from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field

from models import AssignmentStatus, ReportCategory, ReportStatus, TaskStatus


class NGOBase(BaseModel):
    name: str
    contact_email: EmailStr
    city: str


class NGOCreate(NGOBase):
    pass


class NGORead(NGOBase):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class VolunteerBase(BaseModel):
    full_name: str
    email: EmailStr
    phone: str | None = None
    city: str
    latitude: float
    longitude: float
    availability_hours: int = 5
    skill_tags: str = ""
    is_active: bool = True


class VolunteerCreate(VolunteerBase):
    firebase_uid: str | None = None


class VolunteerRead(VolunteerBase):
    id: int
    firebase_uid: str | None = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class ReportBase(BaseModel):
    ngo_id: int
    title: str
    description: str
    category: ReportCategory = ReportCategory.other
    city: str
    latitude: float
    longitude: float
    people_affected: int = Field(default=1, ge=1)
    urgency_hint: int = Field(default=50, ge=0, le=100)
    resource_type: str = "general"


class ReportCreate(ReportBase):
    pass


class ReportRead(ReportBase):
    id: int
    status: ReportStatus
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class TaskBase(BaseModel):
    ngo_id: int
    report_id: int
    title: str
    description: str
    required_volunteers: int = Field(default=1, ge=1)
    skill_required: str = "general"
    latitude: float
    longitude: float
    city: str


class TaskCreate(TaskBase):
    pass


class TaskRead(TaskBase):
    id: int
    priority_score: int
    status: TaskStatus
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class AssignmentRead(BaseModel):
    id: int
    task_id: int
    volunteer_id: int
    distance_km: float
    match_score: int
    status: AssignmentStatus
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class DashboardSummary(BaseModel):
    total_reports: int
    open_tasks: int
    active_volunteers: int
    urgent_tasks: int
    average_priority: float


class MatchRequest(BaseModel):
    task_id: int


class NotificationPayload(BaseModel):
    volunteer_id: int
    title: str
    body: str
