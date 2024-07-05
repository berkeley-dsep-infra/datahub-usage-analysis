## Datahub Usage Analysis (refactor_testing_query_courseid.py)

## Updates

1. **Credential Management**:
   - Removed private credentials from the script. Users must now set (Windows) or export (Mac) their API user ID and key in the command line before running `query_courseid.py`.

   **For Mac (bash)**:
   ```bash
   export APP_ID='your_app_id'
   export APP_KEY='your_app_key'
   ```

   **For Windows (cmd)**:
   ```bash
   set APP_ID='your_app_id'
   set APP_KEY='your_app_key'
   ```

2. **Enhanced Script Structure**:

    - Added a main function to handle argparse in an organized way.
    - The main function also allows for interactive input of the term ID and class names for testing purposes.

3. **Multiple Class Names**:

    - `getCourseInformation` can now accept multiple class names as arguments.

4. **Error Handling Improvements**:

    - Refactored `getCourseInformation` to include two separate functions, `validate_class_name(class_name)` and `normalize_class_name(class_name)`, to handle input errors more effectively.

## Usage

You can run the script in two ways:

1. **Command-Line Mode**:
    ```bash
    python refactor_testing_query_courseid.py 2242 "data8" "compsci189"
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

1. **Using `main` for `argparse`**:
    - Is it acceptable to have the `refactor_testing_query_courseid.py` file implement `main` to handle `argparse`, or would you prefer not to include the `main` method inside this script?
      

2. **Interactive Input Option**:
    -Is it appropriate to keep the interactive input method for term ID and class names? This method could be useful for new users to understand the required arguments.
   

4. **Class-Based Structure**:
    -Would it be better to refactor the script to use a class with methods instead of standalone functions, considering that the primary method to be used by the user is `getCourseInformation`?

