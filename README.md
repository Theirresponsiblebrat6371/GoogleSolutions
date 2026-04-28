# Smart Resource Allocation

Smart Resource Allocation is a community response platform built for NGO coordination. It combines a FastAPI backend for reports, tasks, volunteers, and dashboard summaries with a React frontend for organizer and volunteer workflows.

## Features

- Create and manage community events from the organizer dashboard
- Submit volunteer profiles from the volunteer window
- View submitted volunteers on the admin page
- Contact volunteers from the admin page
- Remove scheduled events from the admin page
- Track reports, tasks, volunteers, and dashboard metrics through the API

## Tech Stack

### Backend

- FastAPI
- SQLAlchemy
- Pydantic
- SQLite by default through `.env`

### Frontend

- React
- Vite

## Project Structure

```text
Google-SolutionChallenge-2026/
├── main.py
├── config.py
├── database.py
├── models.py
├── schemas.py
├── routers/
│   ├── dashboard_routes.py
│   ├── reports.py
│   ├── tasks.py
│   └── volunteers.py
├── services/
├── frontend/
│   ├── src/
│   │   ├── App.jsx
│   │   ├── main.jsx
│   │   └── styles.css
│   └── package.json
└── .env
```

## Environment Variables

The app reads configuration from [`.env`](C:\Users\Adiraj\Desktop\Google-SolutionChallenge-2026\.env:1).

Current defaults include:

```env
DATABASE_URL=sqlite:///./smart_resource.db
APP_PORT=8000
DEFAULT_CITY=Bhilai
MATCH_RADIUS_KM=10
PRIORITY_THRESHOLD=70
DEBUG=true
```

## Backend Setup

From the project root:

```powershell
pip install -r requirements.txt
uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

Backend URLs:

- API root: [http://127.0.0.1:8000](http://127.0.0.1:8000)
- Swagger docs: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

## Frontend Setup

From the `frontend` folder:

```powershell
npm install
npm run dev
```

Vite will print the local frontend URL in the terminal, usually `http://localhost:5173`.

## How To Use

### Organizer Flow

1. Open the organizer login.
2. Review scheduled events and submitted volunteers.
3. Create a new event from the admin form.
4. Remove an event with the `Remove event` button.
5. Use the `Contact` button beside a volunteer to view their email and phone number.

### Volunteer Flow

1. Open the volunteer login.
2. Fill in the volunteer enrollment form.
3. Click `Submit profile`.
4. Log in as admin to see the submitted volunteer appear in the dashboard list.

## API Endpoints

### Reports

- `GET /reports/` - list all reports
- `POST /reports/` - create a report and generate a task

### Tasks

- `GET /tasks/` - list tasks ordered by priority
- `POST /tasks/match` - match volunteers to a task

### Volunteers

- `GET /volunteers/` - list volunteers
- `POST /volunteers/` - create a volunteer

### Dashboard

- `GET /dashboard/summary` - fetch summary metrics

## Notes

- The backend creates database tables automatically on startup in [`main.py`](C:\Users\Adiraj\Desktop\Google-SolutionChallenge-2026\main.py:1).
- The current frontend uses local React state for event creation, volunteer submission, contact actions, and event removal.
- Because the frontend state is local, submitted volunteers and newly created or removed events reset on page refresh unless you connect them to the backend.

## Suggested Next Steps

- Connect the frontend forms to the FastAPI endpoints
- Persist organizer events in the database
- Replace the contact popup with a modal or direct `mailto:` and `tel:` actions
- Add authentication for organizer and volunteer access
