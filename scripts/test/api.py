import os
import requests
import logging
from dotenv import load_dotenv
from helpers import extract_subject_area_and_number, construct_url

# Load environment variables
load_dotenv()

BASE_URL = os.getenv('BASE_URL')

# Configure logging
logging.basicConfig(level=logging.INFO)


# Fetch course information from the Berkeley API, trying both with and without 'C' in the catalog number if needed.
def fetch_course_info(term_id, class_name):
    """
    Args:
        term_id (int): The term ID.
        class_name (str): The class name.
    Returns: dict: The extracted course information or an error message.
    """
    app_id = os.getenv('APP_ID')
    app_key = os.getenv('APP_KEY')

    headers = {
        "app_id": app_id,
        "app_key": app_key,
    }

    # Extract the subject area code and number part from the class name
    subject_area_code, number = extract_subject_area_and_number(class_name)
    
    # Construct the full URL for the API request
    full_url = construct_url(term_id, subject_area_code, number, BASE_URL)

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

    except requests.exceptions.RequestException:
        # If the initial fetch fails, try adding 'C' to the number
        number_with_c = 'C' + number
        full_url_with_c = construct_url(term_id, subject_area_code, number_with_c, BASE_URL)

        try:
            response_with_c = requests.get(full_url_with_c, headers=headers)
            response_with_c.raise_for_status()  # Raise an exception for HTTP errors

            if response_with_c.status_code == 200:
                data = response_with_c.json()['apiResponse']['response']
                classes = data['classes']
                extracted_info = {
                    "display_name": classes[0]['displayName'],
                    "department": classes[0]['course']['subjectArea']['description'],
                    "enrollment_count": sum(section['aggregateEnrollmentStatus']['enrolledCount'] for section in classes)
                }
                return extracted_info

        except requests.exceptions.RequestException as e:
            logging.error(f"Failed to retrieve data. Error: {str(e)}")
            return {"error": f"Failed to retrieve data for the given class name: {class_name}"}

