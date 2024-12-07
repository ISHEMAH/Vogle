import psycopg2
import csv

# Database connection
conn = psycopg2.connect(
    dbname="properties_db",
    user="postgres",
    password="!Mamadivine12345",
    host="localhost",
    port="5432"
)
cursor = conn.cursor()

# Open the CSV file
with open('dataset1.csv', 'r') as file:
    reader = csv.reader(file)
    next(reader)  # Skip the header row
    for row in reader:
        cursor.execute(
            "INSERT INTO properties (name, address, price) VALUES (%s, %s, %s)",
            row
        )

# Commit and close
conn.commit()
cursor.close()
conn.close()