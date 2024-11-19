from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from carters.models import CateringOrder, StaffSchedule, EventPlan
from django.db.models import Q, Count
from django.db.models.functions import TruncMonth
from datetime import datetime, timedelta

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
    # Get the last 6 months of data
    six_months_ago = datetime.now() - timedelta(days=180)
    
    # Get events data by month
    events_by_month = EventPlan.objects.filter(
        event_date__gte=six_months_ago
    ).annotate(
        month=TruncMonth('event_date')
    ).values('month').annotate(
        count=Count('id')
    ).order_by('month')

    # Get orders data by month
    orders_by_month = CateringOrder.objects.filter(
        event_date__gte=six_months_ago
    ).annotate(
        month=TruncMonth('event_date')
    ).values('month').annotate(
        count=Count('id')
    ).order_by('month')

    # Process data for the chart
    months = []
    event_counts = []
    order_counts = []
    
    for month in range(6):
        date = datetime.now() - timedelta(days=30 * (5 - month))
        month_name = date.strftime('%B')
        months.append(month_name)
        
        # Find event count for this month
        event_count = next(
            (item['count'] for item in events_by_month if item['month'].strftime('%B') == month_name),
            0
        )
        event_counts.append(event_count)
        
        # Find order count for this month
        order_count = next(
            (item['count'] for item in orders_by_month if item['month'].strftime('%B') == month_name),
            0
        )
        order_counts.append(order_count)

    context = {
        'upcoming_events': EventPlan.objects.filter(event_date__gte=datetime.now()).order_by('event_date')[:5],
        'recent_orders': CateringOrder.objects.all().order_by('-event_date')[:5],
        'staff_schedules': StaffSchedule.objects.filter(event_date__gte=datetime.now()).order_by('event_date')[:5],
        'chart_data': {
            'months': months,
            'event_counts': event_counts,
            'order_counts': order_counts,
        }
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
