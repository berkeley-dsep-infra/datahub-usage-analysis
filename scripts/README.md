## DataHub Usage Analysis (scripts/test)

## Setup Instructions

1. **Change Directory to the `test` Folder inside the `scripts`**:
```bash
cd /datahub-usage-analysis/scripts/test
```

2. **Run this in the terminal with replace “ “ with your own credentials**:
```bash
export APP_ID='13eb564e'
export APP_KEY=''
```

3. **You can run this to check if credential were correctly set**:
```bash
echo $APP_ID
echo $APP_KEY
```

4. **test by running these commands from the terminal**:

```bash
python course_info_fetcher.py data100 data8 compsci189
```
or intereactivately 

```bash
python course_info_fetcher.py
```
eg.:
Please enter the term ID: 2242
Please enter the class names (separated by commas): data100, data8, comopsci189

Expexted Output:

{
    "title": "Principles & Techniques of Data Science",
    "display_name": "2024 Spring DATA C100 001 LEC 001",
    "department": "Data Science Undergrad Studies",
    "enrollment_count": 1132,
    "instructor_PI": "'Joseph E. Gonzalez', 'Narges Norouzi'"
}
{
    "title": "Foundations of Data Science",
    "display_name": "2024 Spring DATA C8 001 LEC 001",
    "department": "Data Science Undergrad Studies",
    "enrollment_count": 1287,
    "instructor_PI": "'Swupnil K Sahai', 'Muhammad R Khan'"
}
{
    "title": "Introduction to Machine Learning",
    "display_name": "2024 Spring COMPSCI 189 001 LEC 001",
    "department": "Electrical Eng & Computer Sci",
    "enrollment_count": 704,
    "instructor_PI": "'Jonathan Shewchuk'"
}