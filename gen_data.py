import random
import json
from faker import Faker
from datetime import datetime, timedelta
import pandas as pd
import string

# Initialize Faker
faker = Faker()

# Constants for data generation
NUM_AGENTS = 25
NUM_CLIENTS = 100
NUM_TRANSACTIONS = 1000

# Helper function to generate a random datetime between start and end
def random_datetime(start, end):
    """Generate a random datetime between `start` and `end`."""
    return faker.date_time_between(start_date=start, end_date=end)

# Helper function to generate a random transaction code
def generate_transaction_code():
    """Generate a unique transaction code (e.g., TXN-ABC123XYZ)."""
    return f"TXN-{''.join(random.choices(string.ascii_uppercase + string.digits, k=8))}"

# # Generate Agent Table
# agents_data = [
#     {
#         "AgentID": i + 1,
#         "FirstName": faker.first_name(),
#         "LastName": faker.last_name(),
#         "Position": random.choice(["Agent", "Manager"]),
#         "Email": faker.unique.email(),
#         "PhoneNumber": faker.unique.phone_number(),
#         "AdminAccess": random.choice([0, 1]),
#         "HireDate": random_datetime("-5y", "now").isoformat()
#     }
#     for i in range(NUM_AGENTS)
# ]

# # Generate Client Table
# clients_data = [
#     {
#         "ClientID": i + 1,
#         "FirstName": faker.first_name(),
#         "LastName": faker.last_name(),
#         "Email": faker.unique.email(),
#         "PhoneNumber": faker.unique.phone_number(),
#         "Country": faker.country(),
#         "RegistrationDate": random_datetime("-5y", "now").isoformat(),
#         "IsActive": random.choice([0, 1])
#     }
#     for i in range(NUM_CLIENTS)
# ]

# Generate Transaction Table
transactions_data = [
    {
        "TransactionID": i + 1,
        "TransactionCode": generate_transaction_code(),
        "ClientID": random.randint(1, NUM_CLIENTS),
        "ClientFullName": faker.name(),
        "AgentID": random.randint(1, NUM_AGENTS),
        "AgentFullName": faker.name(),
        "TransactionDate": random_datetime("-5y", "now").isoformat(),
        "Amount": round(random.uniform(10, 10000), 2),
        "Currency": random.choice(["USD", "EUR", "GBP", "INR", "AUD", "CAD"]),
        "OriginalCountry": faker.country(),
        "DestinationCountry": faker.country(),
        "Fee": round(random.uniform(1, 50), 2),
        "TransactionStatus": random.choice(["Completed", "Pending", "Failed", "Cancelled"]),
        "StatusDate": random_datetime("-5y", "now").isoformat(),
        "Category": random.choice(["Send", "Receive","Other"]),
        "Icon": faker.image_url(),
        "IsFraudulent": random.choice([0, 1])
    }
    for i in range(NUM_TRANSACTIONS)
]

# Save to CSV files
#agents_df = pd.DataFrame(agents_data)
#clients_df = pd.DataFrame(clients_data)
transactions_df = pd.DataFrame(transactions_data)

#agents_df.to_csv("Agents.csv", index=False)
#clients_df.to_csv("Clients.csv", index=False)
transactions_df.to_csv("transactions_.csv", index=False)

# # Save to JSON files
# with open("Agents.json", "w") as f:
#     json.dump(agents_data, f, indent=4)

# with open("Clients.json", "w") as f:
#     json.dump(clients_data, f, indent=4)

with open("transactions_.json", "w") as f:
    json.dump(transactions_data, f, indent=4)


print("Data generation complete. Files saved as CSV, JSON, and SQL dump.")
