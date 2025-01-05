"""Test Google Cloud Vision API credentials."""
from google.cloud import vision
import io

def test_vision_credentials():
    """Verify that we can create a Vision client with current credentials."""
    try:
        client = vision.ImageAnnotatorClient()
        print('Successfully created Vision client')
        return True
    except Exception as e:
        print(f'Error creating Vision client: {e}')
        return False

if __name__ == '__main__':
    test_vision_credentials()
