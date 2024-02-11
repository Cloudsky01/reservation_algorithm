# Installations steps
- Install the required packages using the following command:
```bash
python3 -m pip install -r requirements.txt
```

# Running the application - Locally
- Run the application using the following command:
```bash
functions-framework --target=schedule
```

# Deploying the application
- Deploy the application using the following command:
```bash
gcloud functions deploy schedule --runtime python39 --trigger-http --allow-unauthenticated
```