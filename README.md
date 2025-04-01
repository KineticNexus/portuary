# Portuary

A modern web application for managing port operations and logistics.

## Features

- Port operations management
- Vessel tracking and scheduling
- Cargo management
- Real-time analytics and reporting
- User authentication and authorization

## Tech Stack

### Backend
- FastAPI (Python 3.11+)
- PostgreSQL
- SQLAlchemy
- Alembic for migrations
- Redis for caching
- Celery for background tasks

### Frontend
- React 18+
- TypeScript
- Vite
- TailwindCSS
- React Query
- Zustand for state management

### DevOps
- Docker
- Docker Compose
- GitHub Actions for CI/CD
- Nginx as reverse proxy

## Getting Started

### Prerequisites

- Python 3.11+
- Node.js 18+
- Docker and Docker Compose
- PostgreSQL 15+

### Development Setup

1. Clone the repository:
```bash
git clone https://github.com/KineticNexus/portuary.git
cd portuary
```

2. Set up the backend:
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: .\venv\Scripts\activate
pip install -r requirements.txt
```

3. Set up the frontend:
```bash
cd frontend
npm install
```

4. Start the development servers:
```bash
# Backend (from backend directory)
uvicorn app.main:app --reload

# Frontend (from frontend directory)
npm run dev
```

5. Visit http://localhost:5173 to see the application

### Docker Setup

1. Build and start the containers:
```bash
docker-compose up -d --build
```

2. Visit http://localhost:8080 to see the application

## Contributing

Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details on our code of conduct and the process for submitting pull requests.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.