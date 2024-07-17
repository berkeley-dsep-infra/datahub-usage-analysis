import re
from helpers import has_digits

#Validate and extract subject area code and catalog number from class name
def validate_class_name(class_name):
    """
    Args: class_name (str): The class name.
    Returns: tuple: A tuple containing the subject area code and catalog number, or an error message.
    """
    if class_name == "unknown":
        return None, "Class name is unknown. Please enter a valid class name."
        
    if not has_digits(class_name):
        return None, f"Class name {class_name} is invalid. Please enter a valid class name."
    
    subject_area_code = re.search(r'([a-zA-Z]+)\d+', class_name).group(1).upper()
    number = ''.join(filter(str.isdigit, class_name))
    
    return (subject_area_code, number), None
