from flask import Flask, request
import uuid
import json
import os
import starkbank
import logging
from starkbank import Transfer

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

SAVE_DIR = './logs'
os.makedirs(SAVE_DIR, exist_ok=True)
os.chmod(SAVE_DIR, 0o777)

LOG_FILE = os.path.join(SAVE_DIR, 'webhooks.log')
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(message)s'
)

# Configure Flask system logs to a separate file
FLASK_LOG_FILE = os.path.join(SAVE_DIR, 'flask.log')
flask_handler = logging.FileHandler(FLASK_LOG_FILE)
flask_handler.setLevel(logging.INFO)
flask_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s %(message)s'))
logging.getLogger('werkzeug').addHandler(flask_handler)
logging.getLogger('werkzeug').propagate = False
app = Flask(__name__)




class TransferCredits:
    def __init__(self):
        self.project = self.start_project()

    def start_project(self):
        project = starkbank.Project(
            environment="sandbox",
            id="6028207048359936",
            private_key=private_key_content
        )

        starkbank.user = project
        return project

    def generate_transfer(self, invoice: object):
        transfer = starkbank.Transfer(
                amount=invoice['amount'],
                bank_code="20018183",  # TED
                branch_code="0001",
                account_number="6341320293482496",
                account_type="payment",
                tax_id="20.018.183/0001-80",
                name="Stark Bank S.A."
            )
        starkbank.transfer.create([transfer])


transfer_credits = TransferCredits()
@app.route('/invoice', methods=['POST'])
def invoice():
    logging.info(f"/invoice: {request.json}")
    print("============================== INVOICE ==============================")
    data = request.json['event']
    if "log" not in data:
        return 'Invalid event data', 400

    if "invoice" not in data['log']:
        return 'No invoice data found', 400

    invoice = data['log']['invoice']
    print(f"Received webhooks: {invoice['id']}, Amount: {invoice['amount']}, type: {data['log']['type']}")
    print(invoice)
    if(data['log']['type'] == "credited"):
        transfer_credits.generate_transfer(invoice)

    return '', 200

@app.route('/transfer', methods=['POST'])
def transfer():
    logging.info(f"/transfer: {request.json}")
    print("============================ Transfer Webhook ============================")
    data = request.json['event']
    if "log" not in data:
        return 'Invalid event data', 400

    if "transfer" not in data['log']:
        return 'No transfer data found', 400

    transfer = data['log']['transfer']
    print(f"Received webhooks: {data}")

    return '', 200


@app.route('/other', methods=['POST'])
def other():
    logging.info(f"/other: {request.json}")
    print("============================ OTHER Webhook ============================")
    data = request.json['event']
    if "log" not in data:
        return 'Invalid event data', 400
    print(f"Received webhooks: {data}")

    return '', 200


if __name__ == '__main__':
    app.run(port=5000)