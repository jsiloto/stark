# Running Locally/Debugging

## Setup your environment
```bash
virtualenv venv
source venv/bin/activate
pip install -r invoice/requirements.txt
pip install -r webhooks/requirements.txt
```

## Running
```bash
# Use separate terminals for each command
ngrok http 5000
python webhooks/webhooks.py
```

# Running with Docker
```bash
docker-compose up -d
tail -f logs/webhooks.log
```
