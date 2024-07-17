import re


#Check if the input string contains any digits.
def has_digits(input_string):
    """
    Args: input_string (str): The input string.
    Returns: bool: True if the input string contains digits, False otherwise.
    """
    return any(char.isdigit() for char in input_string)


# Modify the class name by splitting it into subject area code and number, then add 'C' to the number.
def modify_class_name_with_c(class_name):
    """
    Args: class_name (str): The class name.
    Returns: tuple: A tuple containing the subject area code and catalog number.
    """
    # Extract the subject area code from the class name
    subject_area_code = re.search(r'([a-zA-Z]+)', class_name).group(1).upper()
    # Extract the number part from the class name
    number = ''.join(filter(str.isdigit, class_name))
    # Add 'C' to the number part
    number = 'C' + number
    
    return subject_area_code, number


#Extract the subject area code and catalog number from the class name.
def extract_subject_area_and_number(class_name):
    """
    Args: class_name (str): The class name.
    Returns: tuple: A tuple containing the subject area code and catalog number.
    """
    # Extract the subject area code from the class name
    subject_area_code = re.search(r'([a-zA-Z]+)', class_name).group(1).upper()
    # Extract the number part from the class name
    number = ''.join(filter(str.isdigit, class_name))
    
    return subject_area_code, number
