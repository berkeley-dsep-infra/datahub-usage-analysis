import re
from helpers import has_digits, extract_subject_area_and_number

#Validate and extract subject area code and catalog number from class name.
def validate_class_name(class_name):
    """
    Args: class_name (str): The class name.
    Returns: tuple: A tuple containing the subject area code and catalog number, or an error message.
    """
    # Check if the class name is "unknown"
    if class_name == "unknown":
        return None, "Class name is unknown. Please enter a valid class name."
    
    # Check if the class name contains digits
    if not has_digits(class_name):
        return None, f"Class name {class_name} is invalid. Please enter a valid class name."
        
    else:
        # Use the helper function to extract the subject area code and number
        subject_area_code, number = extract_subject_area_and_number(class_name)
    
    return (subject_area_code, number), None

