FROM python:3.11-slim

WORKDIR /app
COPY webhooks.py .
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "webhooks:app"]