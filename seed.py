from database import Base, SessionLocal, engine
from models import NGO, Report, ReportCategory, Volunteer


def seed():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        if db.query(NGO).first():
            return "Seed data already exists."

        ngo = NGO(name="Community Relief Network", contact_email="ops@crn.org", city="Jamshedpur")
        db.add(ngo)
        db.flush()

        volunteers = [
            Volunteer(
                full_name="Asha Verma",
                email="asha@example.com",
                phone="9000000001",
                city="Jamshedpur",
                latitude=22.8046,
                longitude=86.2029,
                availability_hours=6,
                skill_tags="food,logistics,field",
            ),
            Volunteer(
                full_name="Ravi Kumar",
                email="ravi@example.com",
                phone="9000000002",
                city="Jamshedpur",
                latitude=22.8101,
                longitude=86.2105,
                availability_hours=4,
                skill_tags="medical,health,first aid",
            ),
            Volunteer(
                full_name="Neha Singh",
                email="neha@example.com",
                phone="9000000003",
                city="Jamshedpur",
                latitude=22.7990,
                longitude=86.1950,
                availability_hours=8,
                skill_tags="sanitation,community outreach",
            ),
        ]
        db.add_all(volunteers)

        reports = [
            Report(
                ngo_id=ngo.id,
                title="Emergency food distribution needed",
                description="Fifty families need ration support after flooding.",
                category=ReportCategory.food,
                city="Jamshedpur",
                latitude=22.8055,
                longitude=86.2060,
                people_affected=50,
                urgency_hint=85,
                resource_type="food",
            ),
            Report(
                ngo_id=ngo.id,
                title="Water contamination complaint",
                description="Residents reported unsafe drinking water in a local settlement.",
                category=ReportCategory.health,
                city="Jamshedpur",
                latitude=22.8001,
                longitude=86.1995,
                people_affected=25,
                urgency_hint=80,
                resource_type="medical",
            ),
        ]
        db.add_all(reports)
        db.commit()
        return "Seed data inserted successfully."
    finally:
        db.close()


if __name__ == "__main__":
    print(seed())
