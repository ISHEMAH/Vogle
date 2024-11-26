from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from carters.models import CateringOrder, StaffSchedule, EventPlan
from django.db.models import Q, Count
from django.db.models.functions import TruncMonth, TruncDate
from datetime import datetime, timedelta
import json

def schedule_list(request):
    # Get all schedules
    schedules = StaffSchedule.objects.all().order_by('event_date')
    
    # Get the last 30 days of schedule data
    today = datetime.now()
    thirty_days_ago = today - timedelta(days=30)
    
    # Get schedule counts by date
    schedule_stats = StaffSchedule.objects.filter(
        event_date__gte=thirty_days_ago
    ).annotate(
        date=TruncDate('event_date')
    ).values('date').annotate(
        count=Count('id')
    ).order_by('date')

    # Create a complete date range with zeros for missing dates
    date_dict = {}
    current_date = thirty_days_ago
    while current_date <= today:
        date_str = current_date.strftime('%Y-%m-%d')
        date_dict[date_str] = 0
        current_date += timedelta(days=1)

    # Fill in the actual counts
    for stat in schedule_stats:
        date_str = stat['date'].strftime('%Y-%m-%d')
        if date_str in date_dict:
            date_dict[date_str] = stat['count']

    # Prepare the chart data
    chart_data = {
        'dates': list(date_dict.keys()),
        'counts': list(date_dict.values())
    }

    context = {
        'schedules': schedules,
        'chart_data': json.dumps(chart_data)
    }
    
    return render(request, 'employees/schedule_list.html', context)

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
    # Get all orders
    orders = CateringOrder.objects.all().order_by('event_date')
    
    # Get the last 30 days of order data
    today = datetime.now()
    thirty_days_ago = today - timedelta(days=30)
    
    # Get order counts by date
    order_stats = CateringOrder.objects.filter(
        event_date__gte=thirty_days_ago
    ).annotate(
        date=TruncDate('event_date')
    ).values('date').annotate(
        count=Count('id')
    ).order_by('date')

    # Create a complete date range with zeros for missing dates
    date_dict = {}
    current_date = thirty_days_ago
    while current_date <= today:
        date_str = current_date.strftime('%Y-%m-%d')
        date_dict[date_str] = 0
        current_date += timedelta(days=1)

    # Fill in the actual counts
    for stat in order_stats:
        date_str = stat['date'].strftime('%Y-%m-%d')
        if date_str in date_dict:
            date_dict[date_str] = stat['count']

    # Prepare the chart data
    chart_data = {
        'dates': list(date_dict.keys()),
        'counts': list(date_dict.values())
    }

    context = {
        'orders': orders,
        'chart_data': json.dumps(chart_data)
    }
    
    return render(request, 'employees/order_list.html', context)

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
    # Get the last 6 months
    today = datetime.now()
    six_months_ago = today - timedelta(days=180)
    
    # Get monthly counts for events
    events_by_month = EventPlan.objects.filter(
        event_date__gte=six_months_ago
    ).annotate(
        month=TruncMonth('event_date')
    ).values('month').annotate(
        count=Count('id')
    ).order_by('month')

    # Get monthly counts for orders
    orders_by_month = CateringOrder.objects.filter(
        event_date__gte=six_months_ago
    ).annotate(
        month=TruncMonth('event_date')
    ).values('month').annotate(
        count=Count('id')
    ).order_by('month')

    # Get monthly counts for schedules
    schedules_by_month = StaffSchedule.objects.filter(
        event_date__gte=six_months_ago
    ).annotate(
        month=TruncMonth('event_date')
    ).values('month').annotate(
        count=Count('id')
    ).order_by('month')

    # Create months list for labels
    months = []
    event_counts = []
    order_counts = []
    schedule_counts = []

    # Create a list of all months in the range
    current_month = six_months_ago
    month_dict = {}
    while current_month <= today:
        month_str = current_month.strftime('%B %Y')
        months.append(month_str)
        month_dict[current_month.strftime('%Y-%m')] = {
            'events': 0,
            'orders': 0,
            'schedules': 0
        }
        current_month += timedelta(days=32)
        current_month = current_month.replace(day=1)

    # Fill in the actual counts
    for event in events_by_month:
        month_key = event['month'].strftime('%Y-%m')
        if month_key in month_dict:
            month_dict[month_key]['events'] = event['count']

    for order in orders_by_month:
        month_key = order['month'].strftime('%Y-%m')
        if month_key in month_dict:
            month_dict[month_key]['orders'] = order['count']

    for schedule in schedules_by_month:
        month_key = schedule['month'].strftime('%Y-%m')
        if month_key in month_dict:
            month_dict[month_key]['schedules'] = schedule['count']

    # Convert to lists for the chart
    for month_data in month_dict.values():
        event_counts.append(month_data['events'])
        order_counts.append(month_data['orders'])
        schedule_counts.append(month_data['schedules'])

    # Get recent data for cards
    upcoming_events = EventPlan.objects.filter(
        event_date__gte=today
    ).order_by('event_date')[:5]

    recent_orders = CateringOrder.objects.order_by('-event_date')[:5]

    staff_schedules = StaffSchedule.objects.filter(
        event_date__gte=today
    ).order_by('event_date')[:5]

    # Create chart data dictionary
    chart_data = {
        'months': months,
        'event_counts': event_counts,
        'order_counts': order_counts,
        'schedule_counts': schedule_counts
    }

    context = {
        'chart_data': json.dumps(chart_data),
        'upcoming_events': upcoming_events,
        'recent_orders': recent_orders,
        'staff_schedules': staff_schedules,
    }

    return render(request, 'employees/dashboard.html', context)

def event_list(request):
    # Get all events
    events = EventPlan.objects.all().order_by('event_date')
    
    # Get the last 30 days of event data
    today = datetime.now()
    thirty_days_ago = today - timedelta(days=30)
    
    # Get event counts by date
    event_stats = EventPlan.objects.filter(
        event_date__gte=thirty_days_ago
    ).annotate(
        date=TruncDate('event_date')
    ).values('date').annotate(
        count=Count('id')
    ).order_by('date')

    # Create a complete date range with zeros for missing dates
    date_dict = {}
    current_date = thirty_days_ago
    while current_date <= today:
        date_str = current_date.strftime('%Y-%m-%d')
        date_dict[date_str] = 0
        current_date += timedelta(days=1)

    # Fill in the actual counts
    for stat in event_stats:
        date_str = stat['date'].strftime('%Y-%m-%d')
        if date_str in date_dict:
            date_dict[date_str] = stat['count']

    # Prepare the chart data
    chart_data = {
        'dates': list(date_dict.keys()),
        'counts': list(date_dict.values())
    }

    context = {
        'events': events,
        'chart_data': json.dumps(chart_data)
    }
    
    return render(request, 'employees/event_list.html', context)

def update_event_status(request, event_id):
    if request.method == 'POST':
        event = get_object_or_404(EventPlan, id=event_id)
        new_status = request.POST.get('status')
        if new_status in ['Planned', 'In Progress', 'Completed']:
            event.event_status = new_status
            event.save()
            return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'}, status=400)