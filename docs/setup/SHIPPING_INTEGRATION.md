# Shipping Integration Setup Guide

## Overview
The application uses a dual-carrier shipping system:
1. Australia Post (Primary carrier)
2. Toll Priority (Fallback for oversized packages)

## Australia Post Integration

### Size Limits
Australia Post handles packages within these limits:
- Weight: ≤ 22kg
- Length: ≤ 105cm
- Volume: ≤ 0.25m³

### Setup Steps

1. Register for Australia Post API Access
   - Visit [Australia Post Developer Portal](https://developers.auspost.com.au/)
   - Create a developer account
   - Register your application
   - Request API key and account number

2. Environment Variables
   Add to your `.env` file:
   ```bash
   AUSPOST_API_KEY=your_api_key
   AUSPOST_ACCOUNT_NUMBER=your_account_number
   ```

3. Testing Credentials
   ```python
   # Test your credentials using the AusPost client
   from app.services.shipping.auspost_client import AusPostClient
   
   client = AusPostClient(api_key="your_api_key", account_number="your_account_number")
   account_details = client.get_account_details()
   ```

### API Features
- Get shipping prices
- Create shipments
- Generate shipping labels
- Track packages

## Toll Priority Integration (Future)

### When to Use
Toll Priority handles packages exceeding AusPost limits:
- Weight > 22kg
- Length > 105cm
- Volume > 0.25m³

### Setup Requirements (Pending)
1. Toll account setup needed
2. API credentials required
3. Endpoint configuration
4. Request/response mapping

### Implementation Status
- Basic client structure in place
- Pending actual API integration
- Used as fallback carrier only

## Shipping Router Configuration

### Environment Setup
1. Configure AusPost credentials in `backend/app/routers/shipping.py`:
   ```python
   def get_auspost_client() -> AusPostClient:
       """Dependency injection for AusPost client."""
       return AusPostClient(
           api_key=os.getenv("AUSPOST_API_KEY"),
           account_number=os.getenv("AUSPOST_ACCOUNT_NUMBER")
       )
   ```

2. Update environment variables in `.env`:
   ```bash
   AUSPOST_API_KEY=your_api_key
   AUSPOST_ACCOUNT_NUMBER=your_account_number
   ```

### Carrier Selection Logic
The system automatically selects the appropriate carrier:
1. Checks package dimensions against AusPost limits
2. Uses AusPost for packages within limits
3. Falls back to Toll for oversized packages

## Testing Shipping Integration

### Required Test Data
1. Valid addresses within Australia
2. Package dimensions (both within and exceeding limits)
3. Valid postcodes for origin/destination

### Test Scenarios
1. Standard package shipping via AusPost
2. Oversized package handling (Toll fallback)
3. Shipping price calculations
4. Label generation
5. Tracking number validation

## Troubleshooting

### Common Issues
1. Invalid API credentials
   - Verify API key and account number
   - Check credential permissions
   - Ensure proper environment variable setup

2. Package Size Validation
   - Confirm accurate dimensions
   - Verify unit conversions (kg, cm, m³)
   - Check carrier limits

3. Address Validation
   - Ensure valid Australian addresses
   - Verify postcode format
   - Check delivery zone coverage

### Support Resources
1. [Australia Post API Documentation](https://developers.auspost.com.au/docs)
2. [Australia Post Developer Support](https://developers.auspost.com.au/support)
3. Internal documentation in `backend/app/services/shipping/`

## Security Considerations

1. API Credentials
   - Store securely in environment variables
   - Never commit to version control
   - Rotate regularly
   - Use separate test/production credentials

2. Data Protection
   - Encrypt sensitive shipping data
   - Validate address information
   - Secure label generation and storage

## Next Steps

1. Complete AusPost Integration
   - Register for API access
   - Configure environment variables
   - Test basic shipping operations

2. Future Toll Integration
   - Set up Toll account
   - Implement API integration
   - Configure fallback logic

Remember to keep all API credentials secure and never commit them to version control. Use environment variables for all sensitive information.
