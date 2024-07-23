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
python main.py data8 data100 compsci189
```
or intereactivately 

```bash
python main.py
```
eg.:
Please enter the term ID: 2242
Please enter the class names (separated by commas): data, data100, comopsci189

Expexted Output:

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