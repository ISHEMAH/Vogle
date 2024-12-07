import os
import django
from faker import Faker
import random
from decimal import Decimal
import csv

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'carting.settings')
django.setup()

# Import Django models
from carters.models import CateringOrder, StaffSchedule, EventPlan

# Initialize Faker instance
fake = Faker()

# Define constants for choices
ORDER_STATUS_CHOICES = ['Pending', 'Confirmed', 'Completed']
MENU_ITEMS = [
    "Grilled Chicken", "Caesar Salad", "Spaghetti Carbonara", "Vegetable Stir Fry",
    "Beef Wellington", "Vegan Burger", "Chocolate Cake", "Fruit Platter"
]
EVENT_STATUSES = ['Planned', 'In Progress', 'Completed']
STAFF_MEMBERS = [fake.name() for _ in range(50)]  # Generate a list of 50 unique staff members

# Define the number of records to generate
num_catering_orders = 5000
num_staff_schedules = 2000
num_event_plans = 1000

# File names for CSV exports
catering_orders_file = "catering_orders.csv"
staff_schedules_file = "staff_schedules.csv"
event_plans_file = "event_plans.csv"

# Generate CateringOrder records
print("Generating CateringOrder records...")
catering_orders_data = [
    {
        "client_name": fake.name(),
        "event_date": fake.date_between(start_date='-1y', end_date='+1y'),
        "menu_items": ", ".join(random.sample(MENU_ITEMS, random.randint(1, 5))),  # Randomly pick 1-5 menu items
        "quantity": random.randint(1, 100),  # Random quantity between 1 and 100
        "order_status": random.choice(ORDER_STATUS_CHOICES),
        "total_cost": round(Decimal(random.uniform(50.0, 5000.0)), 2),  # Random cost between $50 and $5000
    }
    for _ in range(num_catering_orders)
]

# Save CateringOrder data to CSV
with open(catering_orders_file, mode="w", newline="", encoding="utf-8") as file:
    writer = csv.DictWriter(file, fieldnames=["client_name", "event_date", "menu_items", "quantity", "order_status", "total_cost"])
    writer.writeheader()
    writer.writerows(catering_orders_data)

print(f"CateringOrder records saved to {catering_orders_file}.")

# Generate StaffSchedule records
print("Generating StaffSchedule records...")
staff_schedules_data = [
    {
        "staff_member": random.choice(STAFF_MEMBERS),  # Random staff member from the list
        "event_date": fake.date_between(start_date='-1y', end_date='+1y'),
        "shift_start": fake.time_object(),  # Random start time
        "shift_end": fake.time_object(),  # Random end time
        "assigned_event": None  # Events can be assigned separately if needed
    }
    for _ in range(num_staff_schedules)
]

# Save StaffSchedule data to CSV
with open(staff_schedules_file, mode="w", newline="", encoding="utf-8") as file:
    writer = csv.DictWriter(file, fieldnames=["staff_member", "event_date", "shift_start", "shift_end", "assigned_event"])
    writer.writeheader()
    writer.writerows(staff_schedules_data)

print(f"StaffSchedule records saved to {staff_schedules_file}.")

# Generate EventPlan records
print("Generating EventPlan records...")
event_plans_data = [
    {
        "event_name": fake.catch_phrase(),
        "event_date": fake.date_between(start_date='-1y', end_date='+1y'),
        "location": fake.address(),
        "number_of_guests": random.randint(10, 500),  # Random number of guests between 10 and 500
        "resources_needed": fake.paragraph(nb_sentences=3),  # Random resources description
        "event_status": random.choice(EVENT_STATUSES)
    }
    for _ in range(num_event_plans)
]

# Save EventPlan data to CSV
with open(event_plans_file, mode="w", newline="", encoding="utf-8") as file:
    writer = csv.DictWriter(file, fieldnames=["event_name", "event_date", "location", "number_of_guests", "resources_needed", "event_status"])
    writer.writeheader()
    writer.writerows(event_plans_data)

print(f"EventPlan records saved to {event_plans_file}.")
