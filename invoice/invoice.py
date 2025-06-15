import time

import starkbank
# coding: utf-8
import starkbank
from datetime import date, datetime, timedelta, UTC
import random
import faker
import argparse

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


def generate_random_cpf():
    def calculate_digit(numbers):
        s = sum([int(digit) * weight for digit, weight in zip(numbers, range(len(numbers) + 1, 1, -1))])
        d = 11 - s % 11
        return str(d if d < 10 else 0)

    numbers = [str(random.randint(0, 9)) for _ in range(9)]
    numbers.append(calculate_digit(numbers))
    numbers.append(calculate_digit(numbers))
    return "{}{}{}.{}{}{}.{}{}{}-{}{}".format(*numbers)


class InvoiceSender:
    def __init__(self):
        self.project = self.start_project()
        self.database = self.generate_database()

    def start_project(self):
        project = starkbank.Project(
            environment="sandbox",
            id="6028207048359936",
            private_key=private_key_content
        )

        starkbank.user = project
        return project


    def generate_database(self):
        db = []
        fake = faker.Faker()
        for i in range(1000):
            fakename = fake.name()
            random_tax_id = generate_random_cpf()
            db.append([fakename, random_tax_id])

        return db

    def generate_random_invoice(self):
        fakename, tax_id = random.choice(self.database)
        invoice = starkbank.Invoice(
            amount=23571,  # R$ 235,71
            name=fakename,
            tax_id=tax_id,
            due=datetime.now(UTC) + timedelta(hours=1),
            expiration=timedelta(hours=3).total_seconds(),
            fine=5,  # 5%
            interest=2.5,  # 2.5% per month
            tags=["immediate"],
        )
        return invoice


    def send_invoices(self):
        invoices = []
        for _ in range(random.randint(8, 12)):
            invoices.append(self.generate_random_invoice())
        starkbank.invoice.create(invoices)


def main():
    parser = argparse.ArgumentParser(description="Send invoices")
    parser.add_argument("--recurrent", action="store_true", help="Run in recurrent mode")
    args = parser.parse_args()

    sender = InvoiceSender()
    if args.recurrent:
        print("Recurrent mode selected")
        while True:
            sender.send_invoices()
            time.sleep(3 * 60 * 60)  # wait 3 hours
        #
    else:
        sender.send_invoices()


if __name__ == "__main__":
    main()

# WEBHOOK_URL = "http://receiver:5000/webhook"
#
# def run():
#     while True:
#         payload = {"timestamp": datetime.utcnow().isoformat(), "message": "Hello from sender"}
#         try:
#             r = requests.post(WEBHOOK_URL, json=payload)
#             print(f"[{datetime.now()}] Sent webhook: {r.status_code}")
#         except Exception as e:
#             print(f"Failed to send webhook: {e}")
#         time.sleep(3 * 60 * 60)  # wait 3 hours
#
# if __name__ == "__main__":
#     run()