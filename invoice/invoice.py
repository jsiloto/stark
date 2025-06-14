import starkbank
# coding: utf-8
import starkbank
from datetime import date, datetime, timedelta

# Get your private key from an environment variable or an encrypted database.
# This is only an example of a private key content. You should use your own key.
private_key_content = """
-----BEGIN EC PARAMETERS-----
BgUrgQQACg==
-----END EC PARAMETERS-----
-----BEGIN EC PRIVATE KEY-----
MHQCAQEEIHX3joDOT1x+Wgf9JKh+UykiuBFSOnNk93Z2p1WhfOHXoAcGBSuBBAAK
oUQDQgAE9yvqkZBi2bp+y8JUYolrS1OVCJ94ICrrvfBJl+vavZBSeZ0dLkqu5zMW
3JzTFaGqN9MSfydn3RnMqkPSYrdhzA==
-----END EC PRIVATE KEY-----
"""

project = starkbank.Project(
    environment="sandbox",
    id="6028207048359936",
    private_key=private_key_content
)

starkbank.user = project

from datetime import datetime, timedelta, UTC


invoices = starkbank.invoice.create([
    starkbank.Invoice(
        amount=23571,  # R$ 235,71
        name="Buzz Aldrin",
        tax_id="012.345.678-90",
        due=datetime.now(UTC) + timedelta(hours=1),
        expiration=timedelta(hours=3).total_seconds(),
        fine=5,  # 5%
        interest=2.5,  # 2.5% per month
        tags=["immediate"],

    ),
    starkbank.Invoice(
        amount=23571,  # R$ 235,71
        name="Buzz Aldrin",
        tax_id="012.345.678-90",
        due=date(2025, 7, 20),
        expiration=timedelta(hours=3).total_seconds(),
        fine=5,  # 5%
        interest=2.5,  # 2.5% per month
        tags=["scheduled"]
    )
])

for invoice in invoices:
    print(invoice)

import time
import requests
from datetime import datetime

WEBHOOK_URL = "http://receiver:5000/webhook"

def run():
    while True:
        payload = {"timestamp": datetime.utcnow().isoformat(), "message": "Hello from sender"}
        try:
            r = requests.post(WEBHOOK_URL, json=payload)
            print(f"[{datetime.now()}] Sent webhook: {r.status_code}")
        except Exception as e:
            print(f"Failed to send webhook: {e}")
        time.sleep(3 * 60 * 60)  # wait 3 hours

if __name__ == "__main__":
    run()