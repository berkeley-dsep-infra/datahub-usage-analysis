import os
import requests
import logging
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

BASE_URL = os.getenv('BASE_URL')

# Configure logging
logging.basicConfig(level=logging.INFO)

def fetch_course_info(full_url):
    app_id = os.getenv('APP_ID')
    app_key = os.getenv('APP_KEY')

    headers = {
        "app_id": app_id,
        "app_key": app_key,
    }

    try:
        response = requests.get(full_url, headers=headers)
        response.raise_for_status()  # Raise an exception for HTTP errors

        if response.status_code == 200:
            data = response.json()['apiResponse']['response']
            classes = data['classes']
            extracted_info = {
                "display_name": classes[0]['displayName'],
                "department": classes[0]['course']['subjectArea']['description'],
                "enrollment_count": sum(section['aggregateEnrollmentStatus']['enrolledCount'] for section in classes)
            }
            return extracted_info

    except requests.exceptions.RequestException as e:
        logging.error(f"Failed to retrieve data. Error: {str(e)}")
        return None
