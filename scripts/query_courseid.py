import requests
import json
import re

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

    # Get Subject Area Code from Class Name (input from Data Scientist) e.g. data8 -> DATA
    if class_name == "unknown":
        error_string = "Class name is unknown. Please enter a valid class name."
        return_json = json.dumps(error_string, indent=4)
        return error_string
    elif has_digits(class_name) == False:
        error_string = f"Class name {class_name} is invalid. Please enter a valid class name."
        return_json = json.dumps(error_string, indent=4)
        return error_string

    subject_area_code = class_name.split()[0]
    subject_area_code = re.search(r'([a-zA-Z]+)\d+', class_name)
    subject_area_code = subject_area_code.group(1).upper()

    for i in range(len(class_name)):
        if class_name[i].isdigit():
            number = class_name[i:].upper()
            break

    # Get Desired Display Name for the API from Class Name (input from Data Scientist) e.g. data8 -> DATA 8
    desired_display_name = subject_area_code + " " + str(number)

    # Get Course Information from API using the subject-area-code, term-id, page-number, and page-size
    base_url = "https://gateway.api.berkeley.edu/uat/sis/v1/classes?"
    url_params = f"term-id={term_id}&subject-area-code={subject_area_code}&catalog-number={number}&page-number=  {page_number}&page-size={page_size}"
    full_url = base_url + url_params

    headersinput = {
    "app_id": "",
    "app_key": "",
    }

    response = requests.get(full_url, headers = headersinput)

    if response.status_code == 200:
        data = response.json()  # If the response is in JSON format
        data = data['apiResponse']['response']
        print(data)
        classes = data['classes']
        extracted_info = {
            "display_name": data['classes'][0]['displayName'],
            "department": data['classes'][0]['course']['subjectArea']['description'],
            "enrollment_count": sum(section['aggregateEnrollmentStatus']['enrolledCount'] for section in classes)
        }
        # Creating a new JSON object with the extracted information
        return_json = json.dumps(extracted_info, indent=4)
        print(return_json)
        return return_json
        
    elif check_pattern(class_name) == True:
        desired_display_name = extract_pattern(class_name)
        subject_area_code = desired_display_name.split()[0].upper()
        number = desired_display_name.split()[1].upper()
        base_url = "https://gateway.api.berkeley.edu/uat/sis/v1/classes?"
        url_params = f"term-id={term_id}&subject-area-code={subject_area_code}&catalog-number={number}&page-number={page_number}&page-size={page_size}"
        full_url = base_url + url_params

        headersinput = {
        "app_id": "13eb564e",
        "app_key": "74e1f260b527e7655628220a5de615c6",
        }

        response = requests.get(full_url, headers = headersinput)
        if response.status_code == 200:
            data = response.json()  # If the response is in JSON format
            print(data)
            data = data['apiResponse']['response']
            classes = data['classes']
            extracted_info = {
            "display_name": data['classes'][0]['displayName'],
            "department": data['classes'][0]['course']['subjectArea']['description'],
            "enrollment_count": sum(section['aggregateEnrollmentStatus']['enrolledCount'] for section in classes)
        }
            return_json = json.dumps(extracted_info, indent=4)
            print(return_json)
            return return_json
    else:
        number = "C" + number
        desired_display_name = subject_area_code + " " + str(number)
        base_url = "https://gateway.api.berkeley.edu/uat/sis/v1/classes?"
        url_params = f"term-id={term_id}&subject-area-code={subject_area_code}&catalog-number={number}&page-number={page_number}&page-size={page_size}"
        full_url = base_url + url_params

        headersinput = {
        "app_id": "13eb564e",
        "app_key": "74e1f260b527e7655628220a5de615c6",
        }
        response = requests.get(full_url, headers = headersinput)

        if response.status_code == 200:
            data = response.json()  # If the response is in JSON format
            print(data)
            data = data['apiResponse']['response']
            classes = data['classes']
            extracted_info = {
            "display_name": data['classes'][0]['displayName'],
            "department": data['classes'][0]['course']['subjectArea']['description'],
            "enrollment_count": sum(section['aggregateEnrollmentStatus']['enrolledCount'] for section in classes)
        }
            return_json = json.dumps(extracted_info, indent=4)
            print(return_json)
            return return_json
        else:
            error_string = f"Failed to retrieve data for {class_name}. Status code: {response.status_code}"
            return_json = json.dumps(error_string, indent=4)
            print(return_json)
            return return_json




# getCourseInformation("2232", "data8")
# # print("here")

# SP23_Courses = ['data8', 'data100', 'compsci189', 'data140', 'demog180', 'econ140', 'unknown', 'compsci170', 'eecs16b', 'eecs16a', 'envecon118', 'pbhlth142', 'civeng190', 'data101', 'stat88', 'data6', 'physics111b', 'pbhlth251', 'physics88', 'stat157', 'stat159', 'eleng120', 'math124', 'mcellbi163l', 'ds102', 'polsci3', 'eecs127', 'legalst123', 'eps130', 'datasci241', 'polsci88', 'biology1b', 'polsci5', 'stat131', 'pbhlth252', 'civeng200b', 'integbi134l', 'educw142', 'econ148', 'civeng93', 'espmc167', 'legalst190', 'stat135', 'integbi120', 'data4ac', 'econ151', 'econ141', 'stat20', 'econ135', 'cp201a', 'econ172', 'eep153', 'matsci104l', 'cyplan201b', 'econ157', 'ethstd21ac', 'socwel282', 'econ130', 'mcellbi32', 'ethstdc164a', 'datasci203', 'econ143', 'cyplan88', 'envecon147', 'history160', 'demog175', 'integbi32', 'psych198', 'sociol88', 'aresec', 'anthro115', 'espmc105', 'pbhlth196', 'music30', 'pbhlth250c', 'polsci109', 'dighum101', 'mcellbi280', 'artw23ac', 'mcellbi288', 'cogscic131', 'eps256', 'ls88', 'stat150', 'plantbi135','mcellbic117', 'civeng110', 'pbhlth253', 'eps24', 'ethstd22ac', 'data198', 'pbhlth290', 'dighum160']
# for i in SP23_Courses:
#     getCourseInformation("2232", i)

getCourseInformation("2242", "eleng120")
getCourseInformation("2238", "eleng120")


# INTEGBI 134L
# STAT C131A has an A at the end
#get instructor name

# add instructor name to the json output