# Environment Setup Guide

## Python Dependencies
All Python dependencies are managed through `requirements.txt`. To install:
```bash
pip install -r requirements.txt
```

## Required Environment Variables

### Google Cloud Vision API
Required for item detection and image analysis:
```bash
export GOOGLE_APPLICATION_CREDENTIALS="/path/to/service-account-key.json"
```
See [Google Cloud Vision Setup](./google-cloud-vision.md) for detailed instructions.

### Database Configuration
Required for running the application and tests:
```bash
DATABASE_URL="postgresql://user:password@localhost:5432/dbname"
```

### Test Environment
Additional setup required for running tests:
1. Test data directory with sample images (`backend/tests/test_data/`)
2. Valid database connection with test database
3. Google Cloud Vision API credentials
4. Mock credentials for marketplace integrations (eBay, etc.)

## Development Environment
For local development:
```bash
# Core application
DEBUG=true
API_HOST=localhost
API_PORT=8000

# Feature flags
ENABLE_BACKGROUND_JOBS=false
ENABLE_MARKETPLACE_SYNC=false

# Service integrations
EBAY_API_KEY=your_api_key
AUSPOST_API_KEY=your_api_key
```

## Production Environment
Additional variables required for production:
```bash
NODE_ENV=production
DEBUG=false
ENABLE_BACKGROUND_JOBS=true
ENABLE_MARKETPLACE_SYNC=true
```

## Validation
To verify your environment setup:
1. Run health check: `curl http://localhost:8000/health`
2. Check database connection via Prisma: `npx prisma db pull`
3. Verify Google Cloud Vision credentials: Run item detection tests
