import json
import logging
import os
import requests

from helpers import extract_subject_area_and_number, construct_url

BASE_URL = "https://gateway.api.berkeley.edu/uat/sis/v1/classes/sections?"

# Configure logging
logging.basicConfig(level=logging.INFO)


def extract_info_from_response(response):
    data = response.json()['apiResponse']['response']
    class_section = data.get('classSections', [])[0]

    # Extract title, department, display name, and enrollment count
    title = class_section.get('class', {}).get('course', {}).get('title', 'N/A')
    display_name = class_section.get('displayName', 'N/A')
    department = class_section.get('academicOrganization', {}).get('description', 'N/A')
    enrollment_count = class_section.get('enrollmentStatus', {}).get('enrolledCount', 0)

    # Extract primary instructors names
    instructor_PI = ', '.join(
        f"'{instructor['instructor']['names'][0]['formattedName']}'"
        for meeting in class_section.get('meetings', [])
        for instructor in meeting.get('assignedInstructors', [])
        if instructor.get('role', {}).get('code') == 'PI'
    )

    return {
        "title": title,
        "display_name": display_name,
        "department": department,
        "enrollment_count": enrollment_count,
        "instructor_PI": instructor_PI
    }
    

def fetch_course_info(term_id, class_name):
    """
    Fetch course information from the Berkeley API, trying both with and without 'C' in the catalog number if needed.
    Args:
        term_id (int): The term ID.
        class_name (str): The class name.
    Returns: dict: The extracted course information or an error message.
    """
    api_id = os.getenv('APP_ID')
    api_key = os.getenv('APP_KEY')

    headers = {
        "app_id": api_id,
        "app_key": api_key,
    }

    # Extract the subject area code and number part from the class name
    subject_area_code, number = extract_subject_area_and_number(class_name)
    
    # Construct the full URL for the API request
    full_url = construct_url(term_id, subject_area_code, number, BASE_URL)

    try:
        response = requests.get(full_url, headers=headers)
        response.raise_for_status()  # Raise an exception for HTTP errors

        if response.status_code == 200:
            return extract_info_from_response(response)

    except requests.exceptions.RequestException:
        # If the initial fetch fails, try adding 'C' to the number
        number_with_c = 'C' + number
        full_url_with_c = construct_url(term_id, subject_area_code, number_with_c, BASE_URL)

        try:
            response_with_c = requests.get(full_url_with_c, headers=headers)
            response_with_c.raise_for_status()  # Raise an exception for HTTP errors
            return extract_info_from_response(response_with_c)

        except requests.exceptions.RequestException as e:
            logging.error(f"Failed to retrieve data. Error: {str(e)}")
            return {"error": f"Failed to retrieve data for the given class name: {class_name}"}


def get_course_information(term_id, class_name):
    """
    Fetch course information from the Berkeley API.
    Args:
        term_id (int): The term ID.
        class_name (str): The class name.
    Returns: str: JSON string with extracted information or error message.
    """ 
    # Fetch the course information from the API
    result = fetch_course_info(term_id, class_name)

    # Return the result as a JSON string
    return json.dumps(result, indent=4)
