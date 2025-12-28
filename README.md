# Habit Tracker API

A RESTful API for tracking daily and weekly habits, built with Flask and PostgreSQL.

## 📋 Project Overview

The Habit Tracker is a web-based application designed to help users build and maintain positive habits. It provides a simple API to create habits, log completions, and track progress through streaks and statistics.

### Features

- **Habit Management**: Create, update, delete, and archive habits
- **Frequency Options**: Support for daily and weekly habits
- **Completion Logging**: Log habit completions with optional notes
- **Streak Tracking**: Automatic calculation of current streaks
- **Statistics**: View weekly and monthly completion totals
- **Categories**: Organize habits into custom categories

## 🏗️ Architecture

This application uses a 2-tier architecture:

1. **Web Tier**: Flask REST API application
2. **Database Tier**: PostgreSQL database

Both tiers are containerized using Docker and orchestrated with Docker Compose.

## 🛠️ Tech Stack

- **Backend**: Python 3.11, Flask 3.0
- **Database**: PostgreSQL 15
- **ORM**: Flask-SQLAlchemy
- **Containerization**: Docker & Docker Compose
- **WSGI Server**: Gunicorn

## 📁 Project Structure

```
habit-tracker/
├── app/
│   ├── __init__.py          # Application factory
│   ├── models.py             # Database models
│   └── routes/
│       ├── __init__.py
│       ├── categories.py     # Category endpoints
│       ├── habits.py         # Habit endpoints
│       ├── completions.py    # Completion endpoints
│       └── stats.py          # Statistics endpoints
├── Dockerfile                # Web app container config
├── docker-compose.yml        # Multi-container orchestration
├── requirements.txt          # Python dependencies
├── run.py                    # Application entry point
└── README.md
```

## 🚀 Getting Started

### Prerequisites

- Docker and Docker Compose installed
- Git (for cloning the repository)

### Running the Application

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/habit-tracker.git
   cd habit-tracker
   ```

2. **Start the containers**
   ```bash
   docker-compose up --build
   ```

3. **Access the API**
   - The API will be available at `http://localhost:5000`
   - Health check: `http://localhost:5000/health`

4. **Stop the containers**
   ```bash
   docker-compose down
   ```

### Running Locally (without Docker)

1. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up PostgreSQL and update the connection string in `app/__init__.py`

4. Run the application:
   ```bash
   python run.py
   ```

## 📡 API Endpoints

### Categories

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/categories` | Get all categories |
| GET | `/api/categories/<id>` | Get a category by ID |
| POST | `/api/categories` | Create a new category |
| PUT | `/api/categories/<id>` | Update a category |
| DELETE | `/api/categories/<id>` | Delete a category |

### Habits

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/habits` | Get all habits (with optional filters) |
| GET | `/api/habits/<id>` | Get a habit by ID |
| POST | `/api/habits` | Create a new habit |
| PUT | `/api/habits/<id>` | Update a habit |
| DELETE | `/api/habits/<id>` | Delete a habit |
| GET | `/api/habits/<id>/streak` | Get current streak |
| GET | `/api/habits/<id>/stats` | Get habit statistics |

### Completions

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/habits/<id>/completions` | Get completions for a habit |
| POST | `/api/habits/<id>/completions` | Log a completion |
| DELETE | `/api/completions/<id>` | Delete a completion |

### Statistics

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/stats/summary` | Get summary of all habits |
| GET | `/api/stats/weekly` | Get weekly totals |
| GET | `/api/stats/monthly` | Get monthly totals |

## 📝 Example API Usage

### Create a Category
```bash
curl -X POST http://localhost:5000/api/categories \
  -H "Content-Type: application/json" \
  -d '{"name": "Health"}'
```

### Create a Habit
```bash
curl -X POST http://localhost:5000/api/habits \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Morning Exercise",
    "description": "30 minutes of exercise",
    "frequency": "daily",
    "category_id": 1
  }'
```

### Log a Completion
```bash
curl -X POST http://localhost:5000/api/habits/1/completions \
  -H "Content-Type: application/json" \
  -d '{
    "completed_date": "2025-01-01",
    "notes": "Completed 30 minute jog"
  }'
```

### Get Statistics Summary
```bash
curl http://localhost:5000/api/stats/summary
```

## 🗄️ Database Schema

### Tables

**categories**
- `id` (SERIAL, PRIMARY KEY)
- `name` (VARCHAR(50), NOT NULL, UNIQUE)

**habits**
- `id` (SERIAL, PRIMARY KEY)
- `name` (VARCHAR(100), NOT NULL)
- `description` (TEXT)
- `frequency` (VARCHAR(10), NOT NULL) - 'daily' or 'weekly'
- `category_id` (INTEGER, FOREIGN KEY)
- `is_active` (BOOLEAN, DEFAULT TRUE)
- `created_at` (TIMESTAMP)

**completions**
- `id` (SERIAL, PRIMARY KEY)
- `habit_id` (INTEGER, FOREIGN KEY, NOT NULL)
- `completed_date` (DATE, NOT NULL)
- `notes` (TEXT)
- `created_at` (TIMESTAMP)
- UNIQUE constraint on (habit_id, completed_date)

## 🔜 Future Improvements

- [ ] Add user authentication
- [ ] Implement longest streak tracking
- [ ] Add data visualization endpoints
- [ ] Create automated tests
- [ ] Deploy to cloud platform

## 📄 License

This project is for educational purposes as part of a portfolio project.
