# From Data Generation to MySQL in Docker: A Data Engineer's Journey

As a data analyst diving into the world of data engineering, I recently set out to automate data generation and mount it inside a MySQL Docker container. This post walks through the process, from generating mock data with Python to setting up MySQL in Docker, aimed at fellow data professionals who are exploring data engineering.

## Step 1: Understanding the Need for Synthetic Data

Data is the foundation of any analytics project, but obtaining real-world data can be challenging due to privacy, compliance, and availability constraints. Generating realistic mock data is a great way to test workflows, pipelines, and visualizations without relying on sensitive information. 

I needed a dataset that mimicked real-world transactions, including agents, clients, and transactions between them. By leveraging the `Faker` library and Python, I could automate data creation, ensuring randomness and variation for a more realistic dataset.

## Step 2: Generating Mock Data with Python

I wrote a Python script using `Faker` and `pandas` to generate synthetic transactions. The script creates datasets for Agents, Clients, and Transactions, each containing relevant attributes. Here's a breakdown of the script:

### 1. Importing Libraries and Setting Constants
```python
import random
import json
from faker import Faker
from datetime import datetime, timedelta
import pandas as pd
import string

faker = Faker()
NUM_AGENTS = 25
NUM_CLIENTS = 100
NUM_TRANSACTIONS = 1000
```
This section imports necessary libraries and initializes the Faker module, which helps generate realistic dummy data. `pandas` is used to store and manipulate data, while `random` ensures variability in the generated content.

### 2. Defining Helper Functions
```python
def random_datetime(start, end):
    return faker.date_time_between(start_date=start, end_date=end)

def generate_transaction_code():
    return f"TXN-{''.join(random.choices(string.ascii_uppercase + string.digits, k=8))}"
```
These functions help generate random timestamps and unique transaction codes for the dataset. The transaction code mimics what financial institutions use to track transactions.

### 3. Creating Agents and Clients Data
```python
agents_data = [
    {
        "AgentID": i + 1,
        "FirstName": faker.first_name(),
        "LastName": faker.last_name(),
        "Position": random.choice(["Agent", "Manager"]),
        "Email": faker.unique.email(),
        "PhoneNumber": faker.unique.phone_number(),
        "AdminAccess": random.choice([0, 1]),
        "HireDate": random_datetime("-5y", "now").isoformat()
    }
    for i in range(NUM_AGENTS)
]

clients_data = [
    {
        "ClientID": i + 1,
        "FirstName": faker.first_name(),
        "LastName": faker.last_name(),
        "Email": faker.unique.email(),
        "PhoneNumber": faker.unique.phone_number(),
        "Country": faker.country(),
        "RegistrationDate": random_datetime("-5y", "now").isoformat(),
        "IsActive": random.choice([0, 1])
    }
    for i in range(NUM_CLIENTS)
]
```
This section generates sample data for agents and clients. Each agent has an assigned role, email, and phone number, while each client has a unique country of residence.

### 4. Creating Transactions Data
```python
transactions_data = [
    {
        "TransactionID": i + 1,
        "TransactionCode": generate_transaction_code(),
        "ClientID": random.randint(1, NUM_CLIENTS),
        "AgentID": random.randint(1, NUM_AGENTS),
        "TransactionDate": random_datetime("-5y", "now").isoformat(),
        "Amount": round(random.uniform(10, 10000), 2),
        "Currency": random.choice(["USD", "EUR", "GBP", "INR", "AUD", "CAD"]),
        "DestinationCountry": faker.country(),
        "Fee": round(random.uniform(1, 50), 2),
        "TransactionStatus": random.choice(["Completed", "Pending", "Failed", "Cancelled"]),
        "StatusDate": random_datetime("-5y", "now").isoformat(),
        "Category": random.choice(["Send", "Receive","ME"]),
        "IsFraudulent": random.choice([0, 1])
    }
    for i in range(NUM_TRANSACTIONS)
]
```
Each transaction links a client to an agent and includes financial details such as amount, currency, and transaction status.

### 5. Saving Data to Files
```python
agents_df = pd.DataFrame(agents_data)
clients_df = pd.DataFrame(clients_data)
transactions_df = pd.DataFrame(transactions_data)

agents_df.to_csv("Agents.csv", index=False)
clients_df.to_csv("Clients.csv", index=False)
transactions_df.to_csv("Transactions.csv", index=False)

with open("Agents.json", "w") as f:
    json.dump(agents_data, f, indent=4)

with open("Clients.json", "w") as f:
    json.dump(clients_data, f, indent=4)

with open("Transactions.json", "w") as f:
    json.dump(transactions_data, f, indent=4)
```
This section saves generated data as CSV and JSON files for further use.

### 6. Generating SQL Dump
```python
with open("mysql_dump.sql", "w") as sql_file:
    sql_file.write("""
CREATE TABLE Agents (
    AgentID INT PRIMARY KEY,
    FirstName VARCHAR(50),
    LastName VARCHAR(50),
    Position VARCHAR(20),
    Email VARCHAR(100) UNIQUE,
    PhoneNumber VARCHAR(50) UNIQUE,
    AdminAccess TINYINT,
    HireDate DATETIME
);

CREATE TABLE Clients (
    ClientID INT PRIMARY KEY,
    FirstName VARCHAR(50),
    LastName VARCHAR(50),
    Email VARCHAR(100) UNIQUE,
    PhoneNumber VARCHAR(50) UNIQUE,
    Country VARCHAR(50),
    RegistrationDate DATETIME,
    IsActive TINYINT
);

CREATE TABLE Transactions (
    TransactionID INT PRIMARY KEY,
    TransactionCode VARCHAR(50) UNIQUE,
    ClientID INT,
    AgentID INT,
    TransactionDate DATETIME,
    Amount DECIMAL(10, 2),
    Currency VARCHAR(10),
    DestinationCountry VARCHAR(50),
    Fee DECIMAL(5, 2),
    TransactionStatus VARCHAR(20),
    StatusDate DATETIME,
    Category VARCHAR(20),
    IsFraudulent TINYINT,
    FOREIGN KEY (ClientID) REFERENCES Clients(ClientID),
    FOREIGN KEY (AgentID) REFERENCES Agents(AgentID)
);
""")

print("Data generation complete. Files saved as CSV, JSON, and SQL dump.")
```
This section writes an SQL script to create the database schema and insert generated data. The structured format ensures the dataset is relational and follows best database practices.

### Step 3: Setting Up MySQL with Docker
To deploy our generated data into a MySQL database, we use Docker. Below is our docker-compose.yml configuration:

```YAML
version: '3.8'
services:
  mysql:
    image: mysql:latest
    container_name: mysql_container
    env_file:
      - .env
    volumes:
      - ./mysql_dump.sql:/docker-entrypoint-initdb.d/mysql_dump.sql
    ports:
      - "3306:3306"
```
Additionally, we define our .env file with the necessary credentials:

```
MYSQL_ROOT_PASSWORD=root_password
MYSQL_DATABASE=test_db
MYSQL_USER=user
MYSQL_PASSWORD=user_password
```

### Next Steps: Deploying and Expanding Our Project

Now that we have successfully generated data and set up MySQL in Docker, we can further develop our project in several ways:

1. Automating Data Ingestion: We can schedule automatic data generation and ingestion into MySQL using Apache Airflow or a simple cron job.

2. Deploying Docker Image: The MySQL Docker container can be deployed to cloud platforms like AWS, Azure, or Google Cloud using services like Amazon RDS, Azure Database for MySQL, or Google Cloud SQL.

3. Building Analytical Dashboards: Once our dataset is in place, we can use Power BI, Tableau, or Metabase to build insightful dashboards and monitor transactions.

4. Machine Learning for Fraud Detection: With a labeled dataset including fraudulent transactions, we can train machine learning models to predict and prevent fraud in real-time.

### What We Learned

By going through this exercise, we learned:

How to generate synthetic data with Python’s Faker library.

- The importance of structuring and saving data in various formats (CSV, JSON, SQL).

- How to deploy and manage a MySQL database using Docker.

- Ways to expand and deploy our project in real-world applications.

- This project provided hands-on experience in bridging data analytics with data engineering, laying the groundwork for more advanced data pipeline development.

Do you have other ideas to improve or expand this workflow? Let’s discuss in the comments!



