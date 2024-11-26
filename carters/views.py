# carters/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from .forms import CateringOrderForm, StaffScheduleForm, EventPlanForm
from .models import StaffSchedule, CateringOrder, EventPlan, Employee
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .serializers import (
    CateringOrderSerializer, 
    StaffScheduleSerializer,
    EventPlanSerializer,
    EmployeeSerializer
)

# Dashboard View
def dashboard(request):
    # Simple analytics (counts)
    total_orders = CateringOrder.objects.count()
    total_events = EventPlan.objects.count()
    total_staff = StaffSchedule.objects.count()

    context = {
        'total_orders': total_orders,
        'total_events': total_events,
        'total_staff': total_staff,
    }
    return render(request, 'carters/dashboard.html', context)

# Catering Order Views
def order(request):
    orders = CateringOrder.objects.all()
    return render(request, 'carters/order.html', {'orders': orders})

def order_create(request):
    if request.method == 'POST':
        form = CateringOrderForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('order')
    else:
        form = CateringOrderForm()
    return render(request, 'carters/order_form.html', {'form': form})

def order_update(request, pk):
    order = get_object_or_404(CateringOrder, pk=pk)
    if request.method == 'POST':
        form = CateringOrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('order')
    else:
        form = CateringOrderForm(instance=order)
    return render(request, 'carters/order_form.html', {'form': form})

def order_delete(request, pk):
    order = get_object_or_404(CateringOrder, pk=pk)
    if request.method == 'POST':
        order.delete()
        return redirect('order')
    return render(request, 'carters/order_confirm_delete.html', {'order': order})

def order_update_status(request, pk):
    if request.method == 'POST':
        order = get_object_or_404(CateringOrder, pk=pk)
        new_status = request.POST.get('status')
        if new_status in ['Pending', 'Confirmed', 'Completed']:
            order.order_status = new_status
            order.save()
            return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'}, status=400)

# Staff Schedule Views
def staff_list(request):
    staff_schedules = StaffSchedule.objects.all()
    return render(request, 'carters/staff_list.html', {'staff_schedules': staff_schedules})

def staff_create(request):
    if request.method == 'POST':
        form = StaffScheduleForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('staff_list')
    else:
        form = StaffScheduleForm()
    return render(request, 'carters/staff_form.html', {'form': form})

def staff_update(request, pk):
    staff = get_object_or_404(StaffSchedule, pk=pk)
    if request.method == 'POST':
        form = StaffScheduleForm(request.POST, instance=staff)
        if form.is_valid():
            form.save()
            return redirect('staff_list')
    else:
        form = StaffScheduleForm(instance=staff)
    return render(request, 'carters/staff_form.html', {'form': form})

def staff_delete(request, pk):
    staff = get_object_or_404(StaffSchedule, pk=pk)
    if request.method == 'POST':
        staff.delete()
        return redirect('staff_list')
    return render(request, 'carters/staff_confirm_delete.html', {'staff': staff})

# Event Plan Views
def event_list(request):
    events = EventPlan.objects.all()
    return render(request, 'carters/event_list.html', {'events': events})

def event_create(request):
    if request.method == 'POST':
        form = EventPlanForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('event_list')
    else:
        form = EventPlanForm()
    return render(request, 'carters/event_form.html', {'form': form})

def event_update(request, pk):
    event = get_object_or_404(EventPlan, pk=pk)
    if request.method == 'POST':
        form = EventPlanForm(request.POST, instance=event)
        if form.is_valid():
            form.save()
            return redirect('event_list')
    else:
        form = EventPlanForm(instance=event)
    return render(request, 'carters/event_form.html', {'form': form})

def event_delete(request, pk):
    event = get_object_or_404(EventPlan, pk=pk)
    if request.method == 'POST':
        event.delete()
        return redirect('event_list')
    return render(request, 'carters/event_confirm_delete.html', {'event': event})

def event_update_status(request, pk):
    if request.method == 'POST':
        event = get_object_or_404(EventPlan, pk=pk)
        new_status = request.POST.get('status')
        if new_status in ['Planned', 'In Progress', 'Completed']:
            event.event_status = new_status
            event.save()
            return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'}, status=400)

def landing_page(request):
    return render(request , 'carters/landing_page.html')

# Add these viewsets to your existing views.py
class CateringOrderViewSet(viewsets.ModelViewSet):
    queryset = CateringOrder.objects.all()
    serializer_class = CateringOrderSerializer
    permission_classes = [IsAuthenticated]

class StaffScheduleViewSet(viewsets.ModelViewSet):
    queryset = StaffSchedule.objects.all()
    serializer_class = StaffScheduleSerializer
    permission_classes = [IsAuthenticated]

class EventPlanViewSet(viewsets.ModelViewSet):
    queryset = EventPlan.objects.all()
    serializer_class = EventPlanSerializer
    permission_classes = [IsAuthenticated]

class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    permission_classes = [IsAuthenticated]