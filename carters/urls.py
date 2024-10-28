# carters/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.landing_page, name='landing_page'),
    path('dashboard/', views.dashboard, name='dashboard'),

    # Catering Orders
    path('orders/', views.order_list, name='order_list'),
    path('orders/create/', views.order_create, name='order_create'),
    path('orders/update/<int:pk>/', views.order_update, name='order_update'),
    path('orders/delete/<int:pk>/', views.order_delete, name='order_delete'),
    path('orders/update-status/<int:pk>/', views.order_update_status, name='order_update_status'),

    # Staff Schedules
    path('staff/', views.staff_list, name='staff_list'),
    path('staff/create/', views.staff_create, name='staff_create'),
    path('staff/update/<int:pk>/', views.staff_update, name='staff_update'),
    path('staff/delete/<int:pk>/', views.staff_delete, name='staff_delete'),

    # Event Plans
    path('events/', views.event_list, name='event_list'),
    path('events/create/', views.event_create, name='event_create'),
    path('events/update/<int:pk>/', views.event_update, name='event_update'),
    path('events/delete/<int:pk>/', views.event_delete, name='event_delete'),
    path('events/update-status/<int:pk>/', views.event_update_status, name='event_update_status'),
]
