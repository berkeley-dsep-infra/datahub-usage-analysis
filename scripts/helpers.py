import re


def has_digits(input_string):
    """
    Check if the input string contains any digits.
    Args: input_string (str): The input string.
    Returns: bool: True if the input string contains digits, False otherwise.
    """
    return any(char.isdigit() for char in input_string)


def extract_subject_area_and_number(class_name):
    """
    Extract the subject area code and catalog number from the class name.
    Args: class_name (str): The class name.
    Returns: tuple: A tuple containing the subject area code and catalog number.
    """
    # Extract the subject area code from the class name
    subject_area_code = re.search(r'([a-zA-Z]+)', class_name).group(1).upper()
    # Extract the number part from the class name
    number = ''.join(filter(str.isdigit, class_name))
    
    return subject_area_code, number


def construct_url(term_id, subject_area_code, catalog_number, base_url, page_number=1, page_size=100):
    """
    Construct URL parameters for the API request.
    Args:
        term_id (int): The term ID.
        subject_area_code (str): The subject area code.
        catalog_number (str): The catalog number.
        base_url (str): The base URL for the API.
        page_number (int, optional): The page number. Defaults to 1.
        page_size (int, optional): The page size. Defaults to 100.
    Returns: str: The constructed full URL for the API request.
    """
    url_params = f"term-id={term_id}&subject-area-code={subject_area_code}&catalog-number={catalog_number}&page-number={page_number}&page-size={page_size}"
    return base_url + url_params
