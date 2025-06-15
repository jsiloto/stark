FROM python:3.11-slim

WORKDIR /app
COPY invoice.py .
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "invoice.py", "--recurrent"]