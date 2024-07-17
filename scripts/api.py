import os
import requests
import json

BASE_URL = "https://gateway.api.berkeley.edu/uat/sis/v1/classes?"

# Fetch course information from the Berkeley API
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

        # Check if the response status code is 200
        if response.status_code == 200:
            # If the response is successful, extract the course information
            data = response.json()['apiResponse']['response']
            classes = data['classes']
            extracted_info = {
                "display_name": classes[0]['displayName'],
                "department": classes[0]['course']['subjectArea']['description'],
                "enrollment_count": sum(section['aggregateEnrollmentStatus']['enrolledCount'] for section in classes)
            }
            return json.dumps(extracted_info, indent=4)

    except requests.exceptions.RequestException as e:
        error_string = f"Failed to retrieve data. Error: {str(e)}"
        return json.dumps(error_string, indent=4)
