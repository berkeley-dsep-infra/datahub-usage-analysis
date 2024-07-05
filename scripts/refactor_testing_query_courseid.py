import requests
import json
import re
import os
import argparse

def has_digits(input_string):
    """
    Check if the input string contains any digits.
    
    Args:
        input_string (str): The input string to check.
    
    Returns:
        bool: True if the string contains any digits, False otherwise.
    """
    return any(char.isdigit() for char in input_string)

def check_pattern(s):
    """
    Check if the string matches the pattern 'c\d+$'.
    
    Args:
        s (str): The input string to check.
    
    Returns:
        bool: True if the string matches the pattern, False otherwise.
    """
    pattern = re.compile(r'c\d+$')
    match = re.search(pattern, s)
    return match is not None

def extract_pattern(s):
    """
    Extract pattern from the string and format it accordingly.
    
    Args:
        s (str): The input string to extract the pattern from.
    
    Returns:
        str: The formatted string with the extracted pattern.
    """
    pattern = re.compile(r'([a-zA-Z])(\d+)$')
    match = re.search(pattern, s)
    if match:
        char = match.group(1)
        numbers = match.group(2)
        remaining = s[:match.start()]
        return f"{remaining} {char}{numbers}"
    return None

def normalize_class_name(class_name):
    """
    Normalize class name by removing spaces.
    
    Args:
        class_name (str): The class name to normalize.
    
    Returns:
        str: The normalized class name.
    """
    return class_name.replace(" ", "")

def validate_class_name(class_name):
    """
    Validate class name and return subject area code and number.
    
    Args:
        class_name (str): The class name to validate.
    
    Returns:
        tuple: A tuple containing the subject area code and number if valid, or None and an error message if invalid.
    """
    class_name = normalize_class_name(class_name)

    if class_name == "unknown":
        return None, "Class name is unknown. Please enter a valid class name."

    if not has_digits(class_name):
        return None, f"Class name {class_name} is invalid. Please enter a valid class name."

    subject_area_code_match = re.search(r'([a-zA-Z]+)\d+', class_name)
    if not subject_area_code_match:
        return None, f"Class name {class_name} is invalid. Please enter a valid class name."

    subject_area_code = subject_area_code_match.group(1).upper()
    number = ''.join(filter(str.isdigit, class_name))

    return (subject_area_code, number), None

def getCourseInformation(term_id, class_name, page_number=1, page_size=100):
    """
    Get course information from the API using the subject-area-code, term-id, page-number, and page-size.
    
    Args:
        term_id (str): The term ID.
        class_name (str): The class name.
        page_number (int, optional): The page number. Defaults to 1.
        page_size (int, optional): The page size. Defaults to 100.
    
    Returns:
        str: JSON string with extracted information or error message.
    """
    class_info, error_message = validate_class_name(class_name)
    if error_message:
        return json.dumps(error_message, indent=4)

    subject_area_code, number = class_info

    base_url = "https://gateway.api.berkeley.edu/uat/sis/v1/classes?"
    url_params = f"term-id={term_id}&subject-area-code={subject_area_code}&catalog-number={number}&page-number={page_number}&page-size={page_size}"
    full_url = base_url + url_params

    headers = {
        "app_id": os.getenv('APP_ID'),
        "app_key": os.getenv('APP_KEY'),
    }

    response = requests.get(full_url, headers=headers)

    if response.status_code == 200:
        data = response.json()['apiResponse']['response']
        classes = data['classes']
        extracted_info = {
            "display_name": classes[0]['displayName'],
            "department": classes[0]['course']['subjectArea']['description'],
            "enrollment_count": sum(section['aggregateEnrollmentStatus']['enrolledCount'] for section in classes)
        }
        return json.dumps(extracted_info, indent=4)
    
    if check_pattern(class_name):
        desired_display_name = extract_pattern(class_name)
        if not desired_display_name:
            error_string = f"Class name {class_name} is invalid. Please enter a valid class name."
            return json.dumps(error_string, indent=4)
        
        subject_area_code, number = desired_display_name.split()
        full_url = base_url + f"term-id={term_id}&subject-area-code={subject_area_code}&catalog-number={number}&page-number={page_number}&page-size={page_size}"

        response = requests.get(full_url, headers=headers)
        if response.status_code == 200:
            data = response.json()['apiResponse']['response']
            classes = data['classes']
            extracted_info = {
                "display_name": classes[0]['displayName'],
                "department": classes[0]['course']['subjectArea']['description'],
                "enrollment_count": sum(section['aggregateEnrollmentStatus']['enrolledCount'] for section in classes)
            }
            return json.dumps(extracted_info, indent=4)
    
    error_string = f"Failed to retrieve data for {class_name}. Status code: {response.status_code}"
    return json.dumps(error_string, indent=4)

def main():
    """
    Main function to handle command-line arguments or interactive input.
    """
    parser = argparse.ArgumentParser(description="Fetch course information based on term ID and class name.")
    parser.add_argument('term_id', type=str, nargs='?', help="The term ID (e.g., '2232').")
    parser.add_argument('class_names', type=str, nargs='*', help="One or more class names (e.g., 'data8', 'compsci189').")
    
    args = parser.parse_args()
    
    if not args.term_id or not args.class_names:
        # Interactive input
        term_id = input("Please enter the term ID: ")
        class_names = input("Please enter the class names (separated by commas): ").split(',')
        args.term_id = term_id
        args.class_names = [class_name.strip() for class_name in class_names]
    
    for class_name in args.class_names:
        result = getCourseInformation(args.term_id, class_name)
        print(result)

if __name__ == "__main__":
    main()
