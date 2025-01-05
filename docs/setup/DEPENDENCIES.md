# Project Dependencies and Environment Setup

## Core Requirements

### System Requirements
- Python 3.12 (managed via pyenv)
- Node.js (latest LTS version)
- PostgreSQL database server
- Git

### Python Dependencies
Core packages from requirements.txt:
```
fastapi==0.115.6
google-cloud-vision==3.9.0
pillow==11.1.0
rembg==2.0.61
opencv-python-headless==4.10.0.84
numpy==2.0.2
scikit-image==0.25.0
python-dotenv==1.0.1
uvicorn==0.34.0
onnxruntime
python-multipart
```

### Node.js Dependencies
Core packages from package.json:
```json
{
  "dependencies": {
    "@google-cloud/vision": "^4.x",
    "@prisma/client": "^4.16.2",
    "@radix-ui/react-dialog": "^1.1.4",
    "@radix-ui/react-label": "^2.1.1",
    "@radix-ui/react-slider": "^1.2.2",
    "@radix-ui/react-switch": "^1.1.2",
    "@radix-ui/react-toggle": "^1.1.1",
    "@tensorflow/tfjs": "^4.x",
    "@trpc/client": "^10.38.5",
    "@trpc/server": "^10.38.5",
    "next": "^13.x",
    "react": "^18.x",
    "react-dom": "^18.x"
  },
  "devDependencies": {
    "@testing-library/react": "^14.x",
    "eslint": "^8.57.1",
    "jest": "^29.x",
    "typescript": "^5.7.2"
  }
}
```

## Environment Variables

### Required Environment Variables
```bash
# Core Configuration
DATABASE_URL="postgresql://admin:password@localhost:5432/gfgoodsdb"
NEXT_PUBLIC_API_URL=http://localhost:8000
CORS_ALLOWED_ORIGINS=http://localhost:3000

# Google Cloud Vision API
GOOGLE_APPLICATION_CREDENTIALS="/path/to/service-account-key.json"

# Development Settings
DEBUG=true
API_HOST=localhost
API_PORT=8000

# Feature Flags
ENABLE_BACKGROUND_JOBS=false
ENABLE_MARKETPLACE_SYNC=false

# API Keys
EBAY_API_KEY=your_api_key
AUSPOST_API_KEY=your_api_key
```

## Service Dependencies

### Image Processing
- Google Cloud Vision API for image analysis
- Remove.bg API for background removal
- OpenCV for image manipulation
- PIL/Pillow for image processing
- scikit-image for advanced image operations

### Database
- PostgreSQL (transitioning from Prisma to SQLAlchemy)
- Database migration tools (Alembic recommended for SQLAlchemy)

### Marketplace Integration
- eBay API for marketplace listings
- Australia Post API for shipping integration

## Development Tools
- ESLint for JavaScript/TypeScript linting
- Jest for frontend testing
- pytest for backend testing
- TypeScript for type checking
- Prettier for code formatting

## Test Requirements
- Sample test images in `backend/tests/test_data/`
- Mock credentials for marketplace integrations
- Test database instance
- Google Cloud Vision API credentials

## Optional Development Dependencies
- Docker for containerization
- Redis for caching (if implemented)
- Node.js version manager (nvm)
- Python virtual environment (venv)

## Notes
1. The project is transitioning from Prisma to SQLAlchemy for database operations
2. Background jobs and marketplace sync are configurable via feature flags
3. Local development requires both Python and Node.js environments to be set up
4. Test data and credentials are required for running the full test suite
5. Image processing features require multiple service integrations

## Security Considerations
1. Never commit service account keys or API credentials
2. Store sensitive credentials in environment variables or secure vaults
3. Follow the principle of least privilege for service accounts
4. Regularly rotate API keys and credentials
5. Use secure connection strings for database access
