#!/usr/bin/env python3

import argparse
import json
import os
import re
import requests

# Define the base URL as a global variable
BASE_URL = "https://gateway.api.berkeley.edu/uat/sis/v1/classes?"

# Function to check if the input string contains any digits
def has_digits(input_string):
    """
    Check if the input string contains any digits.
    Args: input_string (str): The input string.
    Returns: bool: True if the input string contains digits, False otherwise.
    """
    return any(char.isdigit() for char in input_string)

# Function to check if the string matches the pattern 'c\d+$'
def check_pattern(s):
    """
    Check if the string matches the pattern 'c\d+$'.
    Args: s (str): The input string.
    Returns: bool: True if the string matches the pattern, False otherwise.
    """
    pattern = re.compile(r'c\d+$')
    match = re.search(pattern, s)
    return match is not None

# Function to extract the pattern from the string and format it accordingly
def extract_pattern(s):
    """
    Extract the pattern from the string and format it accordingly.
    Args: s (str): The input string.
    Returns: str: The formatted string.
    """
    pattern = re.compile(r'([a-zA-Z])(\d+)$')
    match = re.search(pattern, s)
    if match:
        char = match.group(1)
        numbers = match.group(2)
        remaining = s[:match.start()]  # Extracts characters before the matched pattern
        return f"{remaining} {char}{numbers}"

# Function to get course information from the API
def getCourseInformation(term_id, class_name, page_number=1, page_size=100):
    """
    Fetch course information from the Berkeley API.
    
    Args:
        term_id (str): The term ID.
        class_name (str): The class name.
        page_number (int, optional): The page number. Defaults to 1.
        page_size (int, optional): The page size. Defaults to 100.
    
    Returns:
        str: JSON string with extracted information or error message.
    """
    # Check if class name is "unknown"
    if class_name == "unknown":
        # If the class name is "unknown", return an error message
        error_string = "Class name is unknown. Please enter a valid class name."
        return json.dumps(error_string, indent=4)
        
    # Check if class name has digits
    elif not has_digits(class_name):
        # If the class name does not contain any digits, return an error message
        error_string = f"Class name {class_name} is invalid. Please enter a valid class name."
        return json.dumps(error_string, indent=4)

    # Extract subject area code from the class name
    subject_area_code = re.search(r'([a-zA-Z]+)\d+', class_name)
    subject_area_code = subject_area_code.group(1).upper()

    # Find the numeric part of the class name
    for i in range(len(class_name)):
        if class_name[i].isdigit():
            number = class_name[i:].upper()
            break

    desired_display_name = subject_area_code + " " + str(number)

    url_params = f"term-id={term_id}&subject-area-code={subject_area_code}&catalog-number={number}&page-number={page_number}&page-size={page_size}"
    full_url = BASE_URL + url_params

    app_id = os.getenv('APP_ID')
    app_key = os.getenv('APP_KEY')

    headers = {
        "app_id": app_id,
        "app_key": app_key,
    }

    print(f"Request URL: {full_url}")  # Debug: Print the full URL

    try:
        response = requests.get(full_url, headers=headers)
        response.raise_for_status()  # Raise an exception for HTTP errors

        # Check if the response status code is 200
        if response.status_code == 200:
            data = response.json()['apiResponse']['response']
            classes = data['classes']
            extracted_info = {
                "display_name": classes[0]['displayName'],
                "department": classes[0]['course']['subjectArea']['description'],
                "enrollment_count": sum(section['aggregateEnrollmentStatus']['enrolledCount'] for section in classes)
            }
            # Creating a new JSON object with the extracted information
            return_json = json.dumps(extracted_info, indent=4)
            print(return_json)
            return return_json
        else:
            print(f"Unexpected status code: {response.status_code}")
            print(response.json())

    except requests.exceptions.RequestException as e:
        error_string = f"Failed to retrieve data for {class_name}. Error: {str(e)}"
        print(error_string)  # Debug: Print the error
        return json.dumps(error_string, indent=4)

    # Check if class name matches pattern 'c\d+$'
    if check_pattern(class_name):
        # If the class name matches the pattern 'c\d+$', extract and reformat the pattern in the class name
        desired_display_name = extract_pattern(class_name)
        subject_area_code, number = desired_display_name.split()
        full_url = BASE_URL + f"term-id={term_id}&subject-area-code={subject_area_code}&catalog-number={number}&page-number={page_number}&page-size={page_size}"

        print(f"Request URL for pattern match: {full_url}")  # Debug: Print the full URL for pattern match

        try:
            response = requests.get(full_url, headers=headers)
            response.raise_for_status()  # Raise an exception for HTTP errors

            # Check if the response status code is 200
            if response.status_code == 200:
                data = response.json()['apiResponse']['response']
                classes = data['classes']
                extracted_info = {
                    "display_name": classes[0]['displayName'],
                    "department": classes[0]['course']['subjectArea']['description'],
                    "enrollment_count": sum(section['aggregateEnrollmentStatus']['enrolledCount'] for section in classes)
                }
                return json.dumps(extracted_info, indent=4)
            else:
                print(f"Unexpected status code: {response.status_code}")
                print(response.json())

        except requests.exceptions.RequestException as e:
            error_string = f"Failed to retrieve data for {class_name}. Error: {str(e)}"
            print(error_string)  # Debug: Print the error
            return json.dumps(error_string, indent=4)

    # If the class name does not match the pattern, modify it to include 'C'
    number = "C" + number
    desired_display_name = subject_area_code + " " + str(number)
    full_url = BASE_URL + f"term-id={term_id}&subject-area-code={subject_area_code}&catalog-number={number}&page-number={page_number}&page-size={page_size}"

    print(f"Request URL for non-pattern match: {full_url}")  # Debug: Print the full URL for non-pattern match

    try:
        response = requests.get(full_url, headers=headers)
        response.raise_for_status()  # Raise an exception for HTTP errors

        # Check if the response status code is 200
        if response.status_code == 200:
            data = response.json()['apiResponse']['response']
            classes = data['classes']
            extracted_info = {
                "display_name": classes[0]['displayName'],
                "department": classes[0]['course']['subjectArea']['description'],
                "enrollment_count": sum(section['aggregateEnrollmentStatus']['enrolledCount'] for section in classes)
            }
            return json.dumps(extracted_info, indent=4)
        else:
            print(f"Unexpected status code: {response.status_code}")
            print(response.json())

    except requests.exceptions.RequestException as e:
        error_string = f"Failed to retrieve data for {class_name}. Error: {str(e)}"
        print(error_string)  # Debug: Print the error
        return json.dumps(error_string, indent=4)

# Main function to handle command-line arguments and fetch course information
def main():
    """
    Main function to handle command-line arguments or interactive input.
    """
    parser = argparse.ArgumentParser(description="Fetch course information based on term ID and class name.")
    parser.add_argument('term_id', type=int, nargs='?', default=2232, help="The term ID (e.g., '2232').")
    parser.add_argument('class_names', type=str, nargs='*', help="One or more class names (e.g., 'data8', 'compsci189').")
    
    args = parser.parse_args()
    
    # Check if the necessary environment variables are set
    if not os.getenv('APP_ID') or not os.getenv('APP_KEY'):
        print("Error: The environment variables APP_ID and APP_KEY must be set.")
        return

    # Check if class names are provided
    if not args.class_names:
        # If class names are not provided, prompt the user to input them interactively
        term_id = input("Please enter the term ID: ")
        class_names = input("Please enter the class names (separated by commas): ").split(',')
        args.term_id = int(term_id)
        args.class_names = [class_name.strip() for class_name in class_names]

    # Loop through each class name and fetch information
    for class_name in args.class_names:
        result = getCourseInformation(args.term_id, class_name)
        print(result)

if __name__ == "__main__":
    main()
