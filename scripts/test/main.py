#!/usr/bin/env python3

import argparse
import logging
import os

from api import get_course_information


# Configure logging
logging.basicConfig(level=logging.INFO)


def main():
    """
    Main function to handle command-line arguments and fetch course information.
    """
    parser = argparse.ArgumentParser(description="Fetch course information based on term ID and class name.")
    
    parser.add_argument('term_id',
                        type=int,
                        nargs='?',
                        default=2232,
                        help="The term ID (e.g., 2232).")
    
    parser.add_argument('class_names',
                        type=str,
                        nargs='*',
                        help="One or more class names (e.g., data8, compsci189).")

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
