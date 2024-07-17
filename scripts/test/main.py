#!/usr/bin/env python3

import argparse
import os
import json
import re
import logging
from api import fetch_course_info, BASE_URL
#from validation import validate_class_name
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)


#Fetch course information from the Berkeley API.
def get_course_information(term_id, class_name):
    """
    Fetch course information from the Berkeley API.
    Args:
        term_id (int): The term ID.
        class_name (str): The class name.
    Returns: str: JSON string with extracted information or error message.
    """

    """#Validate the class name and extract the subject area code and catalog number
    Maybe won't need validaiton since we implemented try in api.py
    validation_result, error = validate_class_name(class_name)
    if error:
        # If there's an error in validation, return the error message as JSON
        return json.dumps(error, indent=4)
    # Unpack the validation result into subject area code and catalog number
    subject_area_code, catalog_number = validation_result
    # Fetch the course information from the API
    result = fetch_course_info(term_id, f"{subject_area_code}{catalog_number}")"""
    
        
    # Fetch the course information from the API
    result = fetch_course_info(term_id, class_name)

    # Return the result as a JSON string
    return json.dumps(result, indent=4)


def main():
    """
    Main function to handle command-line arguments and fetch course information.
    """
    parser = argparse.ArgumentParser(description="Fetch course information based on term ID and class name.")
    parser.add_argument('term_id', type=int, nargs='?', default=2232, help="The term ID (e.g., '2232').")
    parser.add_argument('class_names', type=str, nargs='*', help="One or more class names (e.g., 'data8', 'compsci189').")

    args = parser.parse_args()

    if not os.getenv('APP_ID') or not os.getenv('APP_KEY'):
        logging.error("The environment variables APP_ID and APP_KEY must be set.")
        return

    if not args.class_names:
        term_id = input("Please enter the term ID: ")
        class_names = input("Please enter the class names (separated by commas): ").split(',')
        args.term_id = int(term_id)
        args.class_names = [class_name.strip() for class_name in class_names]

    for class_name in args.class_names:
        result = get_course_information(args.term_id, class_name)
        print(result)

if __name__ == "__main__":
    main()
