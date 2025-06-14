FROM python:3.11-slim

WORKDIR /app
COPY sender.py .

RUN pip install requests

CMD ["python", "sender.py"]