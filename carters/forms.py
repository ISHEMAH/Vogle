from django import forms
from .models import CateringOrder, StaffSchedule, EventPlan

class CateringOrderForm(forms.ModelForm):
    class Meta:
        model = CateringOrder
        fields = '__all__'

class StaffScheduleForm(forms.ModelForm):
    class Meta:
        model = StaffSchedule
        fields = '__all__'

class EventPlanForm(forms.ModelForm):
    class Meta:
        model = EventPlan
        fields = '__all__'

# from django import forms
# from .models import CateringOrder, StaffSchedule, EventPlan

# class CateringOrderForm(forms.ModelForm):
#     class Meta:
#         model = CateringOrder
#         fields = ['client_name', 'event_type', 'number_of_guests', 'event_date', 'menu_items', 'special_requests']

# class StaffScheduleForm(forms.ModelForm):
#     class Meta:
#         model = StaffSchedule
#         fields = ['staff_member', 'shift_date', 'start_time', 'end_time', 'assigned_task']

# class EventPlanForm(forms.ModelForm):
#     class Meta:
#         model = EventPlan
#         fields = ['event_name', 'event_date', 'location', 'budget', 'description']
