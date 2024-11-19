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

