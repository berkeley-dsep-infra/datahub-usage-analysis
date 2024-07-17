import re

#Check if the input string contains any digits
def has_digits(input_string):
    """
    Args: input_string (str): The input string.
    Returns: bool: True if the input string contains digits, False otherwise.
    """
    return any(char.isdigit() for char in input_string)

#Check if the string matches the pattern 'c\d+$'
def check_pattern(s):
    """
    Args: s (str): The input string.
    Returns: bool: True if the string matches the pattern, False otherwise.
    """
    pattern = re.compile(r'c\d+$')
    match = re.search(pattern, s)
    return match is not None

#Extract the pattern from the string and format it accordingly
def extract_pattern(s):
    """
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
