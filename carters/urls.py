# carters/urls.py
from django.urls import path
from .views import create_catering_order, create_staff_schedule, create_event_plan, success,landing_page
from . import views  

urlpatterns = [
    path('create-order/', create_catering_order, name='create_order'),
    path('create-schedule/', create_staff_schedule, name='create_schedule'),
    path('create-event/', create_event_plan, name='create_event'),
    path('success/', success, name='success'),
    path('', views.landing_page, name='landing_page'),
]
