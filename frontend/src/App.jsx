import { useState } from "react";

const ngoHighlights = [
  { label: "Open Reports", value: "128" },
  { label: "Urgent Tasks", value: "18" },
  { label: "Active Volunteers", value: "342" },
  { label: "Avg Match Time", value: "12 min" }
];

const initialEvents = [
  {
    id: 1,
    name: "Blood donation camp",
    location: "Bhilai",
    date: "Tomorrow",
    time: "10:00 AM",
    details: "Blood donation volunteers and donor registration support needed in Bhilai."
  },
  {
    id: 2,
    name: "Feeding street dogs",
    location: "Bhilai",
    date: "Friday",
    time: "2:00 PM",
    details: "Volunteer support needed in Bhilai for feeding rounds and supply distribution."
  },
  {
    id: 3,
    name: "Sanitation cleanup sprint",
    location: "Ward 7",
    date: "Saturday",
    time: "8:00 AM",
    details: "Sanitation response team needed for Ward 7 cleanup and awareness."
  }
];

const enrollmentFields = [
  { label: "Full Name", placeholder: "Enter volunteer name" },
  { label: "Email", placeholder: "Enter email address" },
  { label: "Phone", placeholder: "Enter contact number" },
  { label: "Skills", placeholder: "Food, medical, sanitation" }
];

const initialVolunteerProfiles = [];

export default function App() {
  const [role, setRole] = useState("volunteer");
  const [loggedInRole, setLoggedInRole] = useState(null);
  const [events, setEvents] = useState(initialEvents);
  const [volunteerProfiles, setVolunteerProfiles] = useState(initialVolunteerProfiles);
  const [eventForm, setEventForm] = useState({
    name: "",
    location: "",
    date: "",
    time: "",
    details: ""
  });
  const [volunteerForm, setVolunteerForm] = useState({
    fullName: "",
    email: "",
    phone: "",
    skills: "",
    availability: "Weekdays Evenings",
    preferredCity: ""
  });

  const handleEventChange = (field, value) => {
    setEventForm((current) => ({
      ...current,
      [field]: value
    }));
  };

  const handleCreateEvent = (event) => {
    event.preventDefault();
    if (!eventForm.name || !eventForm.location || !eventForm.date || !eventForm.time) {
      return;
    }

    const nextEvent = {
      id: Date.now(),
      name: eventForm.name,
      location: eventForm.location,
      date: eventForm.date,
      time: eventForm.time,
      details: eventForm.details || `${eventForm.name} needs volunteers in ${eventForm.location}.`
    };

    setEvents((current) => [nextEvent, ...current]);
    setEventForm({
      name: "",
      location: "",
      date: "",
      time: "",
      details: ""
    });
  };

  const handleVolunteerChange = (field, value) => {
    setVolunteerForm((current) => ({
      ...current,
      [field]: value
    }));
  };

  const handleVolunteerSubmit = () => {
    if (
      !volunteerForm.fullName ||
      !volunteerForm.email ||
      !volunteerForm.phone ||
      !volunteerForm.skills ||
      !volunteerForm.preferredCity
    ) {
      return;
    }

    const nextVolunteer = {
      id: Date.now(),
      ...volunteerForm
    };

    setVolunteerProfiles((current) => [nextVolunteer, ...current]);
    setVolunteerForm({
      fullName: "",
      email: "",
      phone: "",
      skills: "",
      availability: "Weekdays Evenings",
      preferredCity: ""
    });
  };

  const handleRemoveEvent = (eventId) => {
    setEvents((current) => current.filter((event) => event.id !== eventId));
  };

  if (!loggedInRole) {
    return (
      <div className="page-shell login-shell">
        <section className="login-layout">
          <div className="login-intro">
            <p className="eyebrow">Smart Resource Allocation</p>
            <h1>Sign in to coordinate faster community response.</h1>
            <p className="lede">
              Separate access for field volunteers and NGO organizers keeps
              enrollment, task intake, and operational control clean and focused.
            </p>
            <div className="role-switch">
              <button
                className={role === "volunteer" ? "role-chip active" : "role-chip"}
                onClick={() => setRole("volunteer")}
              >
                Volunteer Login
              </button>
              <button
                className={role === "admin" ? "role-chip active" : "role-chip"}
                onClick={() => setRole("admin")}
              >
                Organizer Login
              </button>
            </div>
          </div>

          <div className="login-card">
            <div className="window-topbar">
              <span className="dot red" />
              <span className="dot amber" />
              <span className="dot green" />
            </div>
            <p className="eyebrow">{role === "admin" ? "Organizer Access" : "Volunteer Access"}</p>
            <h2>{role === "admin" ? "Organizer Login" : "Volunteer Login"}</h2>
            <form
              className="login-form"
              onSubmit={(event) => {
                event.preventDefault();
                setLoggedInRole(role);
              }}
            >
              <label className="field">
                <span>Email</span>
                <input placeholder={role === "admin" ? "organizer@ngo.org" : "volunteer@example.com"} />
              </label>
              <label className="field">
                <span>Password</span>
                <input type="password" placeholder="Enter password" />
              </label>
              <button type="submit" className="login-submit">
                {role === "admin" ? "Open Organizer Window" : "Open Volunteer Window"}
              </button>
            </form>
          </div>
        </section>
      </div>
    );
  }

  return (
    <div className="page-shell">
      <header className="hero">
        <div>
          <p className="eyebrow">Smart Resource Allocation</p>
          <h1>Coordinate urgent NGO response with live volunteer matching.</h1>
          <p className="lede">
            Prioritize critical community needs, dispatch nearby volunteers, and
            keep operations visible from a single dashboard.
          </p>
        </div>
        <div className="hero-card">
          <h2>Live Operations Snapshot</h2>
          <div className="stats-grid">
            {ngoHighlights.map((item) => (
              <div key={item.label} className="stat-card">
                <span>{item.label}</span>
                <strong>{item.value}</strong>
              </div>
            ))}
          </div>
        </div>
      </header>

      <main className={loggedInRole === "admin" ? "single-window" : "single-window"}>
        {loggedInRole === "admin" ? (
          <section className="window-panel admin-window">
            <div className="window-topbar">
              <span className="dot red" />
              <span className="dot amber" />
              <span className="dot green" />
            </div>
            <div className="panel-heading">
              <div>
                <p className="eyebrow">Organizer Window</p>
                <h2>NGO Operations Dashboard</h2>
              </div>
              <div className="header-actions">
                <button className="secondary-button" onClick={() => setLoggedInRole(null)}>
                  Log out
                </button>
                <button>Review urgent queue</button>
              </div>
            </div>
            <div className="stats-grid">
              {ngoHighlights.map((item) => (
                <div key={item.label} className="stat-card">
                  <span>{item.label}</span>
                  <strong>{item.value}</strong>
                </div>
              ))}
            </div>
            <ul className="timeline">
              <li>
                <strong>Food shortage</strong>
                <span>Priority 91 • 5 volunteers requested • Bhilai</span>
              </li>
              <li>
                <strong>Medical camp support</strong>
                <span>Priority 88 • 3 volunteers requested • Bhilai</span>
              </li>
              <li>
                <strong>Sanitation audit</strong>
                <span>Priority 72 • 2 volunteers requested • Ward 7</span>
              </li>
            </ul>
            <section className="event-section">
              <div className="section-header">
                <p className="eyebrow">Add New Event</p>
                <h3>Create a new community event</h3>
              </div>
              <form className="event-form" onSubmit={handleCreateEvent}>
                <label className="field">
                  <span>Event Name</span>
                  <input
                    placeholder="Community food distribution drive"
                    value={eventForm.name}
                    onChange={(event) => handleEventChange("name", event.target.value)}
                  />
                </label>
                <label className="field">
                  <span>Location</span>
                  <input
                    placeholder="Bhilai"
                    value={eventForm.location}
                    onChange={(event) => handleEventChange("location", event.target.value)}
                  />
                </label>
                <label className="field">
                  <span>Date</span>
                  <input
                    type="date"
                    value={eventForm.date}
                    onChange={(event) => handleEventChange("date", event.target.value)}
                  />
                </label>
                <label className="field">
                  <span>Time</span>
                  <input
                    type="time"
                    value={eventForm.time}
                    onChange={(event) => handleEventChange("time", event.target.value)}
                  />
                </label>
                <label className="field full-width">
                  <span>Details</span>
                  <textarea
                    rows="4"
                    placeholder="Describe the event purpose, volunteer needs, and logistics."
                    value={eventForm.details}
                    onChange={(event) => handleEventChange("details", event.target.value)}
                  />
                </label>
                <button type="submit">Create Event</button>
              </form>
              <div className="event-list">
                <p className="eyebrow">Scheduled Events</p>
                <ul className="feed admin-feed">
                  {events.map((event) => (
                    <li key={event.id} className="admin-list-item">
                      <span>
                        {event.name} • {event.location} • {event.date} {event.time}
                      </span>
                      <button
                        type="button"
                        className="danger-button"
                        onClick={() => handleRemoveEvent(event.id)}
                      >
                        Remove event
                      </button>
                    </li>
                  ))}
                </ul>
              </div>
              <div className="event-list">
                <p className="eyebrow">Submitted Volunteers</p>
                <ul className="feed admin-feed">
                  {volunteerProfiles.length ? (
                    volunteerProfiles.map((profile) => (
                      <li key={profile.id} className="admin-list-item">
                        <span>
                          {profile.fullName} • {profile.skills} • {profile.preferredCity} • {profile.availability}
                        </span>
                        <button
                          type="button"
                          className="contact-button"
                          onClick={() =>
                            window.alert(
                              `Contact ${profile.fullName}\nEmail: ${profile.email}\nPhone: ${profile.phone}`
                            )
                          }
                        >
                          Contact
                        </button>
                      </li>
                    ))
                  ) : (
                    <li>No volunteer profiles submitted yet.</li>
                  )}
                </ul>
              </div>
            </section>
          </section>
        ) : (
          <section className="window-panel volunteer-window">
            <div className="window-topbar">
              <span className="dot red" />
              <span className="dot amber" />
              <span className="dot green" />
            </div>
            <div className="panel-heading">
              <div>
                <p className="eyebrow">Volunteer Window</p>
                <h2>Volunteer Enrollment</h2>
              </div>
              <div className="header-actions">
                <button className="secondary-button light" onClick={() => setLoggedInRole(null)}>
                  Log out
                </button>
                <button type="button" onClick={handleVolunteerSubmit}>
                  Submit profile
                </button>
              </div>
            </div>
            <form className="enrollment-form">
              {enrollmentFields.map((field) => {
                const fieldMap = {
                  "Full Name": "fullName",
                  Email: "email",
                  Phone: "phone",
                  Skills: "skills"
                };
                const fieldKey = fieldMap[field.label];

                return (
                  <label key={field.label} className="field">
                    <span>{field.label}</span>
                    <input
                      placeholder={field.placeholder}
                      value={volunteerForm[fieldKey]}
                      onChange={(event) => handleVolunteerChange(fieldKey, event.target.value)}
                    />
                  </label>
                );
              })}
              <label className="field">
                <span>Availability</span>
                <select
                  value={volunteerForm.availability}
                  onChange={(event) => handleVolunteerChange("availability", event.target.value)}
                >
                  <option>Weekdays Evenings</option>
                  <option>Weekends</option>
                  <option>Full Time</option>
                </select>
              </label>
              <label className="field">
                <span>Preferred City</span>
                <input
                  placeholder="Bhilai"
                  value={volunteerForm.preferredCity}
                  onChange={(event) => handleVolunteerChange("preferredCity", event.target.value)}
                />
              </label>
            </form>
            <div className="feed-panel">
              <p className="eyebrow">Live Organizer Events</p>
              <ul className="feed">
                {events.map((event) => (
                  <li key={event.id}>
                    <strong>{event.name}</strong>
                    <span>
                      {event.location} • {event.date} {event.time}
                    </span>
                    <span>{event.details}</span>
                  </li>
                ))}
              </ul>
            </div>
          </section>
        )}
      </main>
    </div>
  );
}
