from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='employee_dashboard'),
    path('schedules/', views.schedule_list, name='schedule_list'),
    path('schedules/update/<int:schedule_id>/', views.update_schedule_status, name='update_schedule_status'),
    path('orders/', views.order_list, name='order_list'),
    path('orders/update/<int:order_id>/', views.update_order_status, name='update_order_status'),
    path('events/', views.event_list, name='event_list'),
    path('events/update/<int:event_id>/', views.update_event_status, name='update_event_status'),
]