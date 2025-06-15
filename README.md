# Running Locally/Debugging

## Setup your environment
```bash
virtualenv venv
source venv/bin/activate
pip install -r invoice/requirements.txt
pip install -r webhook/requirements.txt
```

## Running
```bash
# Use separate terminals for each command
ngrok http 5000
python webhook/webhooks.py
```