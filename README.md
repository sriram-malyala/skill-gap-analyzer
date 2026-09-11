# Skill-Gap Analyzer

An AI-powered platform that analyzes student resumes and projects against real job postings to identify skill gaps and generate personalized learning paths.

## Features

- **Resume Parser**: Extracts skills, experience, and education from student resumes (PDF, DOCX, TXT)
- **Project Analyzer**: Analyzes GitHub repositories and project descriptions to identify demonstrated skills
- **Job Posting Ingestion**: Fetches and parses job postings from multiple sources (LinkedIn, Indeed, etc.)
- **Gap Analysis**: Uses AI (OpenAI/Claude) to identify missing skills and competency levels
- **Learning Path Generator**: Creates personalized, prioritized learning recommendations with resources
- **Progress Tracking**: Monitors skill development and tracks completed learning activities
- **Skill Proficiency Levels**: Assesses current and target proficiency for each skill
- **Interactive Dashboard**: Web interface to view analysis, learning paths, and progress

## Quick Start

### Prerequisites

- Python 3.9+
- PostgreSQL 12+
- Redis 6+
- Node.js 18+ (for frontend)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/sriram-malyala/skill-gap-analyzer.git
   cd skill-gap-analyzer
   ```

2. **Backend setup**
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   cp .env.example .env
   # Edit .env with your configuration
   python manage.py migrate
   python manage.py runserver
   ```

3. **Frontend setup**
   ```bash
   cd frontend
   npm install
   npm run dev
   ```

4. **Start with Docker Compose** (optional)
   ```bash
   docker-compose up
   ```

Visit `http://localhost:3000` for the frontend and `http://localhost:8000/api` for the backend API.

## Architecture

```
skill-gap-analyzer/
├── backend/              Django REST API + ML pipeline
│   ├── api/              Core API endpoints
│   ├── ml/               Skill extraction & gap analysis
│   ├── models/           Database models
│   └── utils/            Parser utilities
├── frontend/             React + TypeScript dashboard
│   ├── components/       Reusable UI components
│   ├── pages/            Page components
│   └── services/         API integration
├── ml_models/            Pre-trained models & embeddings
├── tests/                Test suites
└── docker-compose.yml    Local development stack
```

## API Documentation

Full OpenAPI/Swagger docs available at `/api/docs`

Key endpoints:
- `POST /api/resumes/` - Upload and analyze resume
- `POST /api/projects/` - Analyze GitHub project
- `POST /api/jobs/` - Add job posting for analysis
- `GET /api/gaps/{student_id}/` - Get skill gap analysis
- `GET /api/learning-paths/{student_id}/` - Get personalized learning path
- `POST /api/learning-activities/` - Log completed activities

## Workflow

1. **Input Phase**: Student uploads resume and links GitHub projects
2. **Extraction Phase**: System extracts skills, experience, and project details
3. **Analysis Phase**: AI compares against job postings and identifies gaps
4. **Generation Phase**: Personalized learning path with prioritized recommendations
5. **Tracking Phase**: Monitor progress as student completes learning activities

## Technology Stack

### Backend
- **Framework**: Django 4.2 + Django REST Framework
- **Database**: PostgreSQL with SQLAlchemy ORM
- **Cache**: Redis for session & skill cache
- **ML**: Hugging Face Transformers, scikit-learn
- **APIs**: OpenAI GPT-4, LinkedIn/Indeed parsers
- **Task Queue**: Celery for async processing

### Frontend
- **Framework**: React 18 + TypeScript
- **State Management**: Redux Toolkit
- **UI Components**: Material-UI v5
- **Charts**: Recharts for skill visualization
- **Forms**: React Hook Form + Zod validation

### Infrastructure
- **Containerization**: Docker + Docker Compose
- **Web Server**: Gunicorn + Nginx
- **Logging**: Sentry for error tracking
- **Testing**: pytest, Jest

## Usage Examples

### Upload Resume & Analyze

```python
from api.services import SkillExtractor

extractor = SkillExtractor()
resume_skills = extractor.extract_from_file('resume.pdf')
# Returns: {'skills': [...], 'experience_years': {...}, 'education': [...]}
```

### Analyze Skill Gaps

```python
from api.services import GapAnalyzer

analyzer = GapAnalyzer()
gaps = analyzer.analyze(
    student_skills=resume_skills,
    job_posting_id='job_123'
)
# Returns: {
#   'missing_skills': [...],
#   'gap_severity': 'high',
#   'recommendations': [...]
# }
```

### Generate Learning Path

```python
from api.services import LearningPathGenerator

generator = LearningPathGenerator()
path = generator.generate(
    student_id='student_123',
    target_role='Senior Backend Engineer',
    current_skills=resume_skills,
    skill_gaps=gaps
)
# Returns personalized learning path with resources
```

## Configuration

Key environment variables:

```env
# Django
DEBUG=False
SECRET_KEY=your-secret-key
ALLOWED_HOSTS=localhost,127.0.0.1

# Database
DATABASE_URL=postgresql://user:password@localhost:5432/skill_gap_analyzer

# Redis
REDIS_URL=redis://localhost:6379/0

# AI APIs
OPENAI_API_KEY=sk-...
HUGGINGFACE_API_KEY=hf_...

# File Storage
AWS_S3_BUCKET=skill-gap-analyzer-files
AWS_ACCESS_KEY_ID=...
AWS_SECRET_ACCESS_KEY=...

# Frontend
REACT_APP_API_URL=http://localhost:8000/api
```

## Database Schema

Key models:
- `Student`: User profiles
- `Resume`: Uploaded resumes with extracted skills
- `Project`: GitHub projects linked to students
- `JobPosting`: Target job postings
- `SkillGapAnalysis`: Gap analysis results
- `LearningPath`: Personalized learning recommendations
- `LearningActivity`: Progress tracking

## Testing

```bash
# Backend tests
cd backend
pytest tests/ -v --cov=api --cov-report=html

# Frontend tests
cd frontend
npm run test -- --coverage
```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## Roadmap

- [ ] LinkedIn job posting integration
- [ ] AI-powered interview prep based on gaps
- [ ] Skill certification recommendations
- [ ] Peer comparison and benchmarking
- [ ] Mobile app for iOS/Android
- [ ] Video course integration (Coursera, Udemy API)
- [ ] Real-time skill assessment quizzes
- [ ] Job market salary predictions

## License

MIT License - see LICENSE file for details

## Support

- 📖 [Documentation](./docs)
- 💬 [GitHub Discussions](https://github.com/sriram-malyala/skill-gap-analyzer/discussions)
- 🐛 [Report Issues](https://github.com/sriram-malyala/skill-gap-analyzer/issues)

---

**Built with ❤️ to help students achieve their career goals**
