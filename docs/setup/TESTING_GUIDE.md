# Testing Guide

## Overview
This guide outlines the testing requirements, setup, and procedures for the Guilt Free Goods v2.0 project.

## Test Environment Setup

### Required Test Data
1. Sample Images
   - Location: `backend/tests/test_data/`
   - Required files:
     * Sample product images (various sizes/qualities)
     * Images with and without backgrounds
     * Images with text/watermarks
     * Images exceeding size limits

2. Test Database
   - Test database instance required
   - Sample data for all models
   - Migrations must be applied

3. Test Credentials
   ```bash
   # Required in .env.test
   GOOGLE_APPLICATION_CREDENTIALS="/path/to/test-service-account.json"
   AUSPOST_API_KEY="test_api_key"
   AUSPOST_ACCOUNT_NUMBER="test_account"
   EBAY_API_KEY="test_api_key"
   ```

## Running Tests

### Prerequisites
- Python virtual environment activated
- Test dependencies installed
- Test credentials configured
- Test data in place

### Linting and Style Checks
```bash
# JavaScript/TypeScript
npm run lint
npm run lint -- --fix  # Auto-fix issues

# Python
flake8 backend/
black backend/ --check
```

### Unit Tests
```bash
# Backend tests
pytest backend/tests -v

# Frontend tests
npm test
```

### Test Categories

1. Image Processing Tests
   - Requires:
     * Google Cloud Vision credentials
     * Sample images in test_data/
   ```bash
   pytest backend/tests/test_item_detection.py -v
   pytest backend/tests/test_vision_credentials.py -v
   ```

2. Shipping Integration Tests
   - Requires:
     * AusPost test credentials
     * Sample shipping data
   ```bash
   pytest backend/tests/test_shipping.py -v
   ```

3. Database Tests
   - Requires:
     * Test database connection
     * Applied migrations
   ```bash
   pytest backend/tests/test_models.py -v
   ```

4. API Integration Tests
   - Requires:
     * All test credentials
     * Mock external services
   ```bash
   pytest backend/tests/test_api.py -v
   ```

## Test Data Requirements

### Sample Images
Place the following in `backend/tests/test_data/`:
1. product_image_1.jpg (standard product photo)
2. product_image_2.jpg (product with background)
3. product_image_3.jpg (product with text)
4. oversized_product.jpg (large item photo)

### Mock Data
Test fixtures are provided in `backend/tests/conftest.py` for:
- User accounts
- Product listings
- Orders
- Shipping records
- Analytics data

## Mocking External Services

### Google Cloud Vision
```python
# Example mock in tests
@pytest.fixture
def mock_vision_client(mocker):
    return mocker.patch('app.services.image_processing.product_detector.vision.ImageAnnotatorClient')
```

### Australia Post API
```python
# Example mock in tests
@pytest.fixture
def mock_auspost_client(mocker):
    return mocker.patch('app.services.shipping.auspost_client.AusPostClient')
```

## CI/CD Integration

### GitHub Actions
- Automated tests run on pull requests
- Required checks must pass:
  * Lint checks
  * Unit tests
  * Integration tests
  * Type checking

### Test Environment Variables
Required in GitHub Secrets:
```bash
GOOGLE_CLOUD_CREDENTIALS=base64_encoded_credentials
TEST_AUSPOST_API_KEY=test_key
TEST_AUSPOST_ACCOUNT=test_account
TEST_DATABASE_URL=test_db_url
```

## Troubleshooting

### Common Issues

1. Missing Test Data
   - Error: "FileNotFoundError: test_data/product_image_1.jpg not found"
   - Solution: Ensure all required test images are in backend/tests/test_data/

2. Authentication Failures
   - Error: "Authentication failed for service X"
   - Solution: Verify test credentials in .env.test

3. Database Connection Issues
   - Error: "Could not connect to test database"
   - Solution: Check TEST_DATABASE_URL and database status

### Test Debugging

1. Verbose Output
   ```bash
   pytest backend/tests -v --pdb
   ```

2. Coverage Reports
   ```bash
   pytest --cov=backend/app backend/tests
   ```

## Security Considerations

1. Test Credentials
   - Use separate test accounts
   - Never commit real credentials
   - Rotate test credentials regularly

2. Test Data
   - Use anonymized data
   - Clean up test data after runs
   - Don't use production data in tests

## Best Practices

1. Test Organization
   - Group tests by feature
   - Use descriptive test names
   - Include both positive and negative tests

2. Test Independence
   - Each test should be independent
   - Clean up after each test
   - Don't rely on test order

3. Test Coverage
   - Aim for high coverage
   - Focus on critical paths
   - Include edge cases

Remember:
1. Never commit sensitive credentials
2. Keep test data up to date
3. Run tests locally before pushing
4. Monitor test execution times
5. Update tests when adding features

Note: Local test execution may require additional setup. Refer to environment setup guides for complete configuration instructions.
