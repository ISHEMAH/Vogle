# carters/models.py
from django.db import models
from django.utils import timezone

class CateringOrder(models.Model):
    client_name = models.CharField(max_length=255, default='')
    event_date = models.DateField(default=timezone.now)
    menu_items = models.TextField(default='')
    quantity = models.IntegerField(default=1)
    order_status = models.CharField(
        max_length=50,
        choices=[
            ('Pending', 'Pending'),
            ('Confirmed', 'Confirmed'),
            ('Completed', 'Completed')
        ],
        default='Pending'
    )
    total_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return f"Order for {self.client_name} on {self.event_date}"

class StaffSchedule(models.Model):
    staff_member = models.CharField(max_length=255, default='')
    event_date = models.DateField(default=timezone.now)
    shift_start = models.TimeField(default='09:00:00')
    shift_end = models.TimeField(default='17:00:00')
    assigned_event = models.ForeignKey('EventPlan', on_delete=models.CASCADE, null=True, default=None)

    def __str__(self):
        return f"{self.staff_member} - {self.event_date}"

class EventPlan(models.Model):
    event_name = models.CharField(max_length=255, default='')
    event_date = models.DateField(default=timezone.now)
    location = models.CharField(max_length=255, default='')
    number_of_guests = models.IntegerField(default=0)
    resources_needed = models.TextField(default='')
    event_status = models.CharField(
        max_length=50,
        choices=[
            ('Planned', 'Planned'),
            ('In Progress', 'In Progress'),
            ('Completed', 'Completed')
        ],
        default='Planned'
    )

    def __str__(self):
        return self.event_name
