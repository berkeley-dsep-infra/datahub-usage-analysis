## Datahub Usage Analysis (refactor_testing_query_courseid.py)

## Updates

1. **Credential Management**:
   - Removed private credentials from the script. Users must now set (Windows) or export (Mac) their API user ID and key in the command line before running `query_courseid.py`.

   **Datahub Terminal**:
   ```bash
   export APP_ID='your_app_id'
   export APP_KEY='your_app_key'
   ```
    **Verify Credentials From Terminal**:
   ```bash
    echo $APP_ID
    echo $APP_KEY
   ```
   

2. **Enhanced Script Structure**:

    - Added a main function to handle argparse in an organized way.
    - The main function also allows for interactive input of the term ID and class names for testing purposes.

3. **Multiple Class Names**:

    - `getCourseInformation` can now accept multiple class names as arguments.

## Usage

You can run the script in two ways:

1. **Command-Line Mode**:
    ```bash
    python refactor_testing_query_courseid.py 2242 data8 data100 compsci189
    ```
Expected Output:

{
    "display_name": "2024 Spring DATA C8 001",
    "department": "Data Science, Undergraduate",
    "enrollment_count": 1287
}
{
    "display_name": "2024 Spring DATA C100 001",
    "department": "Data Science, Undergraduate",
    "enrollment_count": 1132
}
{
    "display_name": "2024 Spring COMPSCI 189 001",
    "department": "Computer Science",
    "enrollment_count": 704
}
{
    "display_name": "2024 Spring COMPSCI 189 001",
    "department": "Computer Science",
    "enrollment_count": 704
}
(notebook) jovyan@jupyter-jlucarga:~/datahub-usage-analysis/scripts$ 
    ```

2. **Interactive Mode**:
    - Run the script without arguments and follow the prompts:
        ```bash
        python refactor_testing_query_courseid.py
        ```

    - You will be prompted to enter the term ID and class names:
        ```text
        Please enter the term ID: ... (eg: 2242)
        Please enter the class names (separated by commas): ... (eg: data8, compsci189)
        ```
## Questions for Consideration



