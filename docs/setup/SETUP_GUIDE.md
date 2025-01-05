# Development Environment Setup Guide

This guide provides step-by-step instructions for setting up your development environment for the Guilt Free Goods v2.0 project.

## Prerequisites

### System Requirements
- Python 3.12 (managed via pyenv)
- Node.js LTS version
- PostgreSQL database server
- Git

### Required Tools
```bash
# Install system dependencies
sudo apt-get update
sudo apt-get install -y \
  python3-venv \
  python3-pip \
  nodejs \
  npm \
  postgresql \
  postgresql-contrib \
  libpq-dev
```

## Step 1: Python Environment Setup

1. Create and activate virtual environment:
```bash
cd ~/repos/guilt-free-goods-v2.0
python -m venv venv
source venv/bin/activate  # On Windows: .\venv\Scripts\activate
```

2. Upgrade pip and install dependencies:
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

3. Verify Python setup:
```bash
python -c "import fastapi; print(fastapi.__version__)"
```

## Step 2: Node.js Environment Setup

1. Install Node.js dependencies:
```bash
npm install
```

2. Verify Node.js setup:
```bash
npm run lint
```

## Step 3: Database Setup

1. Start PostgreSQL service:
```bash
sudo service postgresql start
```

2. Create database and user:
```sql
sudo -u postgres psql
CREATE DATABASE gfgoodsdb;
CREATE USER admin WITH PASSWORD 'password';
GRANT ALL PRIVILEGES ON DATABASE gfgoodsdb TO admin;
\q
```

## Step 4: Environment Variables

1. Copy example environment file:
```bash
cp .env.example .env
```

2. Update environment variables in `.env`:
```bash
# Core Configuration
DATABASE_URL="postgresql://admin:password@localhost:5432/gfgoodsdb"
NEXT_PUBLIC_API_URL=http://localhost:8000
CORS_ALLOWED_ORIGINS=http://localhost:3000

# Development Settings
DEBUG=true
API_HOST=localhost
API_PORT=8000

# Feature Flags
ENABLE_BACKGROUND_JOBS=false
ENABLE_MARKETPLACE_SYNC=false
```

## Step 5: Google Cloud Vision Setup

1. Set up Google Cloud Vision credentials:
```bash
# Place your service account key file in a secure location
export GOOGLE_APPLICATION_CREDENTIALS="/path/to/service-account-key.json"
```

2. Verify Google Cloud Vision setup:
```bash
# Run vision credentials test
pytest backend/tests/test_vision_credentials.py -v
```

## Step 6: Development Server

1. Start backend server:
```bash
# In one terminal
source venv/bin/activate
cd backend
uvicorn app.main:app --reload --port 8000
```

2. Start frontend development server:
```bash
# In another terminal
npm run dev
```

## Step 7: Verify Installation

1. Check backend API:
```bash
curl http://localhost:8000/health
```

2. Access frontend:
- Open browser at http://localhost:3000

## Common Issues and Solutions

### Python Dependencies
If you encounter issues with Python dependencies:
1. Ensure you're using Python 3.12
2. Try removing and recreating the virtual environment
3. Check for system-level dependencies

### Database Connection
If database connection fails:
1. Verify PostgreSQL is running
2. Check DATABASE_URL in .env
3. Ensure database user has correct permissions

### Node.js Issues
If npm install fails:
1. Clear npm cache: `npm cache clean --force`
2. Delete node_modules: `rm -rf node_modules`
3. Reinstall dependencies: `npm install`

## Testing Setup

1. Install test dependencies:
```bash
pip install pytest pytest-asyncio pytest-cov
```

2. Run tests:
```bash
# Backend tests
pytest backend/tests -v

# Frontend tests
npm test
```

## Development Tools

### Recommended VSCode Extensions
- Python
- ESLint
- Prettier
- SQLTools
- GitLens

### Code Formatting
- Python: Black formatter
- JavaScript/TypeScript: Prettier
- SQL: SQLFormat

## Next Steps

After setup:
1. Review project documentation in `/docs`
2. Check current issues on GitHub
3. Set up pre-commit hooks (optional)
4. Configure IDE settings

## Security Notes

1. Never commit:
- `.env` files
- Service account keys
- API credentials
- Personal tokens

2. Always use:
- Environment variables for sensitive data
- Secure credential storage
- Latest dependency versions

## Support

If you encounter issues:
1. Check existing documentation
2. Review common issues section
3. Contact development team
4. Create a detailed issue on GitHub

Remember to keep all credentials secure and never commit sensitive information to version control.
