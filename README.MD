# HeraHealth Backend API

HeraHealth is a role-based fitness coaching platform for clients, coaches, and administrators. This repository provides the Flask REST API, MySQL data model, JWT authentication, real-time messaging server, migrations, and automated tests used by the [HeraHealth frontend](https://github.com/mtriana14/Workout-WebAPP-FRONTEND).

The API supports the full coaching workflow: client and coach accounts, coach discovery and applications, coaching requests, workout and meal plans, schedules, activity and progress tracking, reviews, notifications, billing records, and administrative reporting.

## Tech stack

- Python 3.11
- Flask and Flask-SQLAlchemy
- MySQL through PyMySQL
- Flask-Migrate/Alembic for schema migrations
- Flask-JWT-Extended and bcrypt for authentication
- Flask-SocketIO with Eventlet for real-time chat
- Flasgger for interactive API documentation
- pytest for automated tests
- Gunicorn for production serving

## Implemented API areas

- Account registration, login/logout, profile updates, password reset, deactivation/reactivation, and optional Google sign-in
- Coach discovery, applications, profiles, availability, coaching requests, and coach/client relationship management
- Workout plans, exercises within plans, assignments to a weekly calendar, and completion tracking
- Meal plans and meal-plan food items
- Strength, cardio, step, and calorie logs with weekly/monthly/yearly aggregates
- Fitness goals, daily check-ins, progress entries, and progress photos
- Coach reviews and in-app notifications
- Saved payment-method metadata, subscriptions, invoices, coach revenue, payment reporting, and refund-status updates
- Real-time client/coach messaging with conversation history
- Admin user, coach, exercise, payment, notification, and platform-report endpoints

Most endpoints are mounted under `/api`. When the server is running, Flasgger exposes interactive API documentation at [http://localhost:5000/apidocs/](http://localhost:5000/apidocs/).

## Project status and known limitations

HeraHealth is a team-built prototype and should not be treated as a production medical or payment service.

- Payment and refund endpoints update HeraHealth's own database records; no external payment processor is integrated.
- Saved billing records contain card brand, expiration, and last-four metadata only. Do not submit or store real card numbers.
- Uploaded profile and progress images are stored on the application filesystem under `static/uploads`; production deployments should use durable object storage.
- The Socket.IO message events identify senders from event data rather than a socket-bound authentication session. Harden this before deploying chat in an untrusted environment.
- Some older compatibility endpoints overlap with newer role-oriented endpoints.

## Project structure

```text
.
├── app/
│   ├── config/          # Database setup
│   ├── controllers/     # Request handlers and business logic
│   ├── middleware/      # JWT and role guards
│   ├── models/          # SQLAlchemy models
│   ├── routes/          # Flask blueprints and URL definitions
│   ├── seeders/         # Optional local sample data
│   └── __init__.py      # Application factory, CORS, JWT, Swagger, Socket.IO
├── migrations/          # Alembic migration history
├── tests/               # pytest suites and fixtures
├── run.py               # Development entry point
├── Procfile             # Gunicorn/Eventlet production command
├── runtime.txt          # Deployment Python version
└── requirements.txt
```

## Local setup

### Prerequisites

- Python 3.11
- A MySQL server and a MySQL user allowed to create/use the application database

### 1. Clone and create a virtual environment

```bash
git clone https://github.com/mtriana14/NEW-WORKOUT-APP-BACK-END-CS490-.git
cd NEW-WORKOUT-APP-BACK-END-CS490-
python -m venv .venv
```

Activate the environment:

```bash
# macOS/Linux
source .venv/bin/activate

# Windows PowerShell
.venv\Scripts\Activate.ps1
```

Install dependencies:

```bash
python -m pip install -r requirements.txt
```

### 2. Create the MySQL database

Connect with the MySQL CLI or another MySQL client and run:

```sql
CREATE DATABASE herahealth
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;
```

Use a dedicated local database user where possible, and grant it access to `herahealth`.

### 3. Configure the environment

Create `.env` in the repository root:

```env
SECRET_KEY=replace-with-a-random-secret
JWT_SECRET_KEY=replace-with-a-different-random-secret

DB_HOST=localhost
DB_PORT=3306
DB_USER=herahealth_user
DB_PASSWORD=replace-with-your-database-password
DB_NAME=herahealth

# Optional: required only for Google sign-in.
GOOGLE_CLIENT_ID=your-google-oauth-client-id

# Optional: add another allowed frontend origin.
CORS_ORIGIN=http://localhost:3000
```

Do not commit `.env` or real credentials.

### 4. Apply migrations

```bash
python -m flask --app run:app db upgrade
```

### 5. Start the API

```bash
python run.py
```

The API starts at [http://localhost:5000](http://localhost:5000). Useful checks:

- `GET /` confirms the service is running.
- `GET /testdb` checks the database connection.
- `/apidocs/` opens the interactive API reference.

## Optional sample data

Seeders exist for local users, coaches, availability, exercises, and coaching requests, but they are intentionally not run automatically. From a Python shell with the application context:

```python
from run import app
from app.seeders.run_seeders import run_all_seeders

with app.app_context():
    run_all_seeders()
```

The sample accounts use a shared development password and must never be loaded into a public or production database.

## Tests

The shared pytest fixture creates and clears a MySQL database named `test_db`. Use a disposable local MySQL instance and never point test credentials at a database containing data you need to keep.

```sql
CREATE DATABASE test_db
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;
```

Set `DB_HOST`, `DB_PORT`, `DB_USER`, and `DB_PASSWORD` for that MySQL instance, then run:

```bash
pytest
```

## Contributors

The previous README's UC ownership table did not accurately reflect the team’s contributions. This summary combines repository evidence with clarification from project participants. Contribution areas overlap, and Git identities, commit counts, and blame totals should not be interpreted as exact or exclusive measures of authorship.

| Contributor | Contribution areas visible in repository history |
| --- | --- |
| Melani Triana | Major backend contributor across the database schema and models, configuration and seed data, authentication and account flows, coach and client workflows, workout and meal planning, fitness goals and check-ins, administrative features, tests, and deployment integration. |
| Kevin Guzman | Substantial contributions across API integration and maintenance, OAuth, plans and calendars, activity and progress tracking, billing and subscriptions, reviews, admin reporting and management, notifications, automated tests, CI, and deployment fixes. |
| Justin Santiago | Contributions to authentication and account behavior, real-time chat, fitness goals, coach/client workflows, workout and meal-plan functionality, and automated tests. |

## Related repository

- [HeraHealth frontend](https://github.com/mtriana14/Workout-WebAPP-FRONTEND)
