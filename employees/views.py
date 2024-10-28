from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from carters.models import CateringOrder, StaffSchedule, EventPlan
from django.db.models import Q

def schedule_list(request):
    schedules = StaffSchedule.objects.select_related('assigned_event').all()
    return render(request, 'employees/schedule_list.html', {'schedules': schedules})

def update_schedule_status(request, schedule_id):
    if request.method == 'POST':
        schedule = get_object_or_404(StaffSchedule, id=schedule_id)
        new_status = request.POST.get('status')
        if new_status in ['Planned', 'In Progress', 'Completed']:
            if schedule.assigned_event:
                schedule.assigned_event.event_status = new_status
                schedule.assigned_event.save()
            return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'}, status=400)

def order_list(request):
    orders = CateringOrder.objects.all()
    return render(request, 'employees/order_list.html', {'orders': orders})

def update_order_status(request, order_id):
    if request.method == 'POST':
        order = get_object_or_404(CateringOrder, id=order_id)
        new_status = request.POST.get('status')
        if new_status in ['Pending', 'Confirmed', 'Completed']:
            order.order_status = new_status
            order.save()
            return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'}, status=400)

def dashboard(request):
    upcoming_events = EventPlan.objects.filter(event_status='Planned').order_by('event_date')[:5]
    recent_orders = CateringOrder.objects.order_by('-event_date')[:5]
    staff_schedules = StaffSchedule.objects.select_related('assigned_event').filter(
        Q(assigned_event__event_status='Planned') | Q(assigned_event__event_status='In Progress')
    ).order_by('event_date')[:5]

    context = {
        'upcoming_events': upcoming_events,
        'recent_orders': recent_orders,
        'staff_schedules': staff_schedules,
    }
    return render(request, 'employees/dashboard.html', context)

def event_list(request):
    events = EventPlan.objects.all().order_by('event_date')
    return render(request, 'employees/event_list.html', {'events': events})

def update_event_status(request, event_id):
    if request.method == 'POST':
        event = get_object_or_404(EventPlan, id=event_id)
        new_status = request.POST.get('status')
        if new_status in ['Planned', 'In Progress', 'Completed']:
            event.event_status = new_status
            event.save()
            return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'}, status=400)
