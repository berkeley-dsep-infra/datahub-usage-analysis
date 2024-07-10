import requests
import json
import re
import os
import argparse

def has_digits(input_string):
    return any(char.isdigit() for char in input_string)

def check_pattern(s):
    pattern = re.compile(r'c\d+$')
    match = re.search(pattern, s)
    return match is not None

def extract_pattern(s):
    pattern = re.compile(r'([a-zA-Z])(\d+)$')
    match = re.search(pattern, s)
    if match:
        char = match.group(1)
        numbers = match.group(2)
        remaining = s[:match.start()]  # Extracts characters before the matched pattern
        return f"{remaining} {char}{numbers}"

def getCourseInformation(term_id, class_name, page_number=1, page_size=100):
    if class_name == "unknown":
        error_string = "Class name is unknown. Please enter a valid class name."
        return json.dumps(error_string, indent=4)
    elif not has_digits(class_name):
        error_string = f"Class name {class_name} is invalid. Please enter a valid class name."
        return json.dumps(error_string, indent=4)

    subject_area_code = re.search(r'([a-zA-Z]+)\d+', class_name)
    subject_area_code = subject_area_code.group(1).upper()

    for i in range(len(class_name)):
        if class_name[i].isdigit():
            number = class_name[i:].upper()
            break

    desired_display_name = subject_area_code + " " + str(number)

    base_url = "https://gateway.api.berkeley.edu/uat/sis/v1/classes?"
    url_params = f"term-id={term_id}&subject-area-code={subject_area_code}&catalog-number={number}&page-number={page_number}&page-size={page_size}"
    full_url = base_url + url_params

    app_id = os.getenv('APP_ID')
    app_key = os.getenv('APP_KEY')

    headers = {
        "app_id": app_id,
        "app_key": app_key,
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
    
    elif check_pattern(class_name):
        desired_display_name = extract_pattern(class_name)
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
    
    else:
        number = "C" + number
        desired_display_name = subject_area_code + " " + str(number)
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
        else:
            error_string = f"Failed to retrieve data for {class_name}. Status code: {response.status_code}"
            return json.dumps(error_string, indent=4)

def main():
    parser = argparse.ArgumentParser(description="Fetch course information based on term ID and class name.")
    parser.add_argument('term_id', type=str, help="The term ID (e.g., '2232').")
    parser.add_argument('class_names', type=str, nargs='*', help="One or more class names (e.g., 'data8', 'compsci189').")
    
    args = parser.parse_args()
    
    if not args.term_id or not args.class_names:
        term_id = input("Please enter the term ID: ")
        class_names = input("Please enter the class names (separated by commas): ").split(',')
        args.term_id = term_id
        args.class_names = [class_name.strip() for class_name in class_names]

    for class_name in args.class_names:
        result = getCourseInformation(args.term_id, class_name)
        print(result)

if __name__ == "__main__":
    main()
