# Packages the eval runner, golden dataset, and reporting layer.
# Accepts env vars: GROQ_API_KEY, SLACK_WEBHOOK_URL, threshold configs.
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .

CMD ["python", "scripts/run_eval.py"]
