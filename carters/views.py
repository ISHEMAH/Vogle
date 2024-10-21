# carters/views.py
from django.shortcuts import render, redirect
from .forms import CateringOrderForm, StaffScheduleForm, EventPlanForm

def create_catering_order(request):
    if request.method == 'POST':
        form = CateringOrderForm(request.POST)
        if form.is_valid():
            form.save()
            print("Data saved successfully")
            return redirect('success')  # Redirect to a success page or another view
    else:
        form = CateringOrderForm()

    return render(request, 'carters/create_catering_order.html', {'form': form})

def create_staff_schedule(request):
    if request.method == 'POST':
        form = StaffScheduleForm(request.POST)
        if form.is_valid():
            form.save()
            print("Data saved successfully")
            return redirect('success')  # Redirect to a success page or another view
    else:
        form = StaffScheduleForm()
    return render(request, 'create_staff_schedule.html', {'form': form})

def create_event_plan(request):
    if request.method == 'POST':
        form = EventPlanForm(request.POST)
        if form.is_valid():
            form.save()
            print("Data saved successfully")
            return redirect('success')  # Redirect to a success page or another view
    else:
        form = EventPlanForm()
    return render(request, 'carters/create_event_plan.html', {'form': form})

def success(request):
    return render(request, 'carters/success.html')
