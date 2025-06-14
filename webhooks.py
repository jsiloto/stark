from flask import Flask, request
import uuid
import json
import os

app = Flask(__name__)

SAVE_DIR = 'webhook_data'
os.makedirs(SAVE_DIR, exist_ok=True)

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    print("Received webhook:", data)

    # Create a unique filename using UUID
    filename = f"{uuid.uuid4()}.json"
    filepath = os.path.join(SAVE_DIR, filename)

    # Save the data to a file
    with open(filepath, 'w') as f:
        json.dump(data, f, indent=2)

    return '', 200

if __name__ == '__main__':
    app.run(port=5000)