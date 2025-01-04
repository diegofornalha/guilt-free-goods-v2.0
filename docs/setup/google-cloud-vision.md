# Setting up Google Cloud Vision Authentication

This guide explains how to set up authentication for the Google Cloud Vision API used in our image recognition service.

## Prerequisites

1. A Google Cloud Platform (GCP) account
2. A GCP project with billing enabled
3. Google Cloud Vision API enabled for your project

## Setup Steps

1. Enable the Cloud Vision API:
   - Go to [Google Cloud Console](https://console.cloud.google.com)
   - Navigate to "APIs & Services" > "Library"
   - Search for "Cloud Vision API"
   - Click "Enable"

2. Create a Service Account:
   - Navigate to "IAM & Admin" > "Service Accounts"
   - Click "Create Service Account"
   - Name: `guilt-free-goods-vision`
   - Role: "Cloud Vision API User"
   - Click "Create"

3. Generate Service Account Key:
   - Click on the created service account
   - Go to "Keys" tab
   - Click "Add Key" > "Create new key"
   - Choose JSON format
   - Download the key file

4. Set up Authentication:

   Option 1: Environment Variable (Recommended for Development)
   ```bash
   export GOOGLE_APPLICATION_CREDENTIALS="/path/to/service-account-key.json"
   ```

   Option 2: Configuration File (Production)
   - Place the JSON key file in a secure location
   - Update your environment configuration to point to the key file

## Usage

The image recognition service (`app/services/image_processing/product_detector.py`) will automatically use the credentials when initialized:

```python
from google.cloud import vision

# The client will automatically use the credentials
client = vision.ImageAnnotatorClient()
```

## Security Notes

1. Never commit service account keys to version control
2. Store credentials securely in environment variables or secure vaults
3. Follow the principle of least privilege when assigning roles
4. Regularly rotate service account keys

## Troubleshooting

Common issues and solutions:

1. Authentication Error:
   - Verify the GOOGLE_APPLICATION_CREDENTIALS path is correct
   - Ensure the service account has the correct permissions
   - Check if the key file is valid JSON

2. API Not Enabled:
   - Verify the Cloud Vision API is enabled in your GCP project
   - Check if billing is enabled for the project

3. Quota Issues:
   - Monitor your API usage in the Google Cloud Console
   - Request quota increases if needed

## Cost Management

- Monitor API usage regularly
- Set up billing alerts
- Use the pricing calculator to estimate costs
- Consider implementing rate limiting for high-traffic scenarios

## Support

For additional help:
- [Google Cloud Vision Documentation](https://cloud.google.com/vision/docs)
- [Authentication Guide](https://cloud.google.com/docs/authentication)
- [Pricing Information](https://cloud.google.com/vision/pricing)
