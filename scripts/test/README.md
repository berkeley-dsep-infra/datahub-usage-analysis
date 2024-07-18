## DataHub Usage Analysis (scripts/test)

## Setup Instructions

1. **Change Directory to the `test` Folder inside the `scripts`**:
```bash
cd /datahub-usage-analysis/scripts/test
```

2. **Instal dot environment from terminal**:
```bash
pip install python-dotenv
```

3. **To check if installed correctly**:
```bash
python -c "import dotenv; print('dotenv is installed and working!')"
```

4. **Run this in the terminal with replace “ “ with your own credentials**:
```bash
export APP_ID='13eb564e'
export APP_KEY=''
export BASE_URL=https://gateway.api.berkeley.edu/uat/sis/v1/classes?
```

5. **You can run this to check if credential were correctly set**:
```bash
echo $APP_ID
echo $APP_KEY
```

6. **Run this command from the terminal**:

```bash
python main.py data8 data100 compsci189
```