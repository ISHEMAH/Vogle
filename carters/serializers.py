from rest_framework import serializers
from .models import CateringOrder, StaffSchedule, EventPlan, Employee

class CateringOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = CateringOrder
        fields = '__all__'

class StaffScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = StaffSchedule
        fields = '__all__'

class EventPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventPlan
        fields = '__all__'

class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = '__all__' 