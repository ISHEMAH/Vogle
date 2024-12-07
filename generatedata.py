import os
import django
from faker import Faker
from random import choice, randint, uniform
from decimal import Decimal

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "carting.settings")  # Update with your Django settings module
django.setup()

from carters.models import CateringOrder, StaffSchedule, EventPlan  # Update with your actual model imports

fake = Faker()

def generate_and_save_catering_orders(n=5, print_records=False):
   
    order_status_choices = ['Pending', 'Confirmed', 'Completed']
    menu_items = ["Grilled Chicken", "Caesar Salad", "Spaghetti Carbonara", "Vegetable Stir Fry"]
    catering_orders = []

    for _ in range(n):
        order = CateringOrder(
            client_name=fake.name(),
            event_date=fake.date_between(start_date='-1y', end_date='+1y'),
            menu_items=", ".join([choice(menu_items) for _ in range(randint(1, 5))]),
            quantity=randint(1, 100),
            order_status=choice(order_status_choices),
            total_cost=round(Decimal(uniform(50.0, 5000.0)), 2),
        )
        catering_orders.append(order)

        if print_records:  
            print({
                "client_name": order.client_name,
                "event_date": order.event_date,
                "menu_items": order.menu_items,
                "quantity": order.quantity,
                "order_status": order.order_status,
                "total_cost": order.total_cost,
            })

    CateringOrder.objects.bulk_create(catering_orders, batch_size=1000)
    print(f"{n} CateringOrder records saved to the database.")

def generate_and_save_staff_schedules(n=5, print_records=False):
    """Generate and save StaffSchedule records."""
    staff_members = [fake.name() for _ in range(50)]  # Adjust as needed
    staff_schedules = []

    for _ in range(n):
        staff_schedule = StaffSchedule(
            staff_member=choice(staff_members),
            event_date=fake.date_between(start_date='-1y', end_date='+1y'),
            shift_start=fake.time(),
            shift_end=fake.time(),
            assigned_event=None,  # Add logic if needed
        )
        staff_schedules.append(staff_schedule)

        if print_records:
            print({
                "staff_member": staff_schedule.staff_member,
                "event_date": staff_schedule.event_date,
                "shift_start": staff_schedule.shift_start,
                "shift_end": staff_schedule.shift_end,
                "assigned_event": staff_schedule.assigned_event,
            })

    StaffSchedule.objects.bulk_create(staff_schedules, batch_size=1000)
    print(f"Generated and saved {n} StaffSchedule records.")

def generate_and_save_event_plans(n=5, print_records=False):
    """Generate and save EventPlan records."""
    event_status_choices = ['Planned', 'In Progress', 'Completed']
    event_plans = []

    for _ in range(n):
        event_plan = EventPlan(
            event_name=fake.catch_phrase(),
            event_date=fake.date_between(start_date='-1y', end_date='+1y'),
            location=fake.address(),
            number_of_guests=randint(10, 500),
            resources_needed=fake.paragraph(nb_sentences=3),
            event_status=choice(event_status_choices),
        )
        event_plans.append(event_plan)

        if print_records:
            print({
                "event_name": event_plan.event_name,
                "event_date": event_plan.event_date,
                "location": event_plan.location,
                "number_of_guests": event_plan.number_of_guests,
                "resources_needed": event_plan.resources_needed,
                "event_status": event_plan.event_status,
            })

    EventPlan.objects.bulk_create(event_plans, batch_size=1000)
    print(f"Generated and saved {n} EventPlan records.")

if __name__ == "__main__":
    print("Generating and saving 500,000 CateringOrder records...")
    generate_and_save_catering_orders(500000, print_records=False)

    print("Generating and saving 500,000 StaffSchedule records...")
    generate_and_save_staff_schedules(500000, print_records=False)

    print("Generating and saving 500,000 EventPlan records...")
    generate_and_save_event_plans(500000, print_records=False)
