#!/usr/bin/env python3

import argparse
import os
import json
import re
from api import fetch_course_info, BASE_URL
from helpers import has_digits, check_pattern, extract_pattern

# Fetch course information from the Berkeley API
def get_course_information(term_id, class_name, page_number=1, page_size=100):
    """
    Args:
        term_id (int): The term ID.
        class_name (str): The class name.
        page_number (int, optional): The page number. Defaults to 1.
        page_size (int, optional): The page size. Defaults to 100.
    Returns: str: JSON string with extracted information or error message.
    """
    # Check if class name is "unknown"
    if class_name == "unknown":
        # If the class name is "unknown", return an error message
        return json.dumps("Class name is unknown. Please enter a valid class name.", indent=4)
    
    # Check if class name has digits
    elif not has_digits(class_name):
        # If the class name does not contain any digits, return an error message
        return json.dumps(f"Class name {class_name} is invalid. Please enter a valid class name.", indent=4)

    # Extract subject area code from the class name
    subject_area_code = re.search(r'([a-zA-Z]+)\d+', class_name).group(1).upper()

    # Find the numeric part of the class name
    for i in range(len(class_name)):
        if class_name[i].isdigit():
            number = class_name[i:].upper()
            break

    desired_display_name = subject_area_code + " " + str(number)

    url_params = f"term-id={term_id}&subject-area-code={subject_area_code}&catalog-number={number}&page-number={page_number}&page-size={page_size}"
    full_url = BASE_URL + url_params

    result = fetch_course_info(full_url)
    if 'Failed to retrieve data' not in result:
        return result
    
    # Check if class name matches pattern 'c\d+$'
    if check_pattern(class_name):
        # If the class name matches the pattern 'c\d+$', extract and reformat the pattern in the class name
        desired_display_name = extract_pattern(class_name)
        subject_area_code, number = desired_display_name.split()
        full_url = BASE_URL + f"term-id={term_id}&subject-area-code={subject_area_code}&catalog-number={number}&page-number={page_number}&page-size={page_size}"
        result = fetch_course_info(full_url)
        if 'Failed to retrieve data' not in result:
            return result
    
    # If the class name does not match the pattern, modify it to include 'C'
    number = "C" + number
    desired_display_name = subject_area_code + " " + str(number)
    full_url = BASE_URL + f"term-id={term_id}&subject-area-code={subject_area_code}&catalog-number={number}&page-number={page_number}&page-size={page_size}"
    return fetch_course_info(full_url)

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

    # Check if term_id or class_names are provided
    if not args.class_names:
        # If not provided, prompt the user for input
        term_id = input("Please enter the term ID: ")
        class_names = input("Please enter the class names (separated by commas): ").split(',')
        args.term_id = int(term_id)
        args.class_names = [class_name.strip() for class_name in class_names]

    # Loop through each class name and fetch information
    for class_name in args.class_names:
        result = get_course_information(args.term_id, class_name)
        print(result)

if __name__ == "__main__":
    main()
