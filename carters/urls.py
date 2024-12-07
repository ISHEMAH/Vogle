# carters/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'api/orders', views.CateringOrderViewSet)
router.register(r'api/staff', views.StaffScheduleViewSet)
router.register(r'api/events', views.EventPlanViewSet)
router.register(r'api/employees', views.EmployeeViewSet)

urlpatterns = [
    path('', views.landing_page, name='landing_page'),
    path('dashboard/', views.dashboard, name='dashboard'),
    

    # Catering Orders
    path('orders/', views.order, name='order_list'),
    path('orders/create/', views.order_create, name='order_create'),
    path('orders/update/<int:pk>/', views.order_update, name='order_update'),
    path('orders/delete/<int:pk>/', views.order_delete, name='order_delete'),
    path('orders/update-status/<int:pk>/', views.order_update_status, name='order_update_status'),

    # Include the router URLs
    path('', include(router.urls)),
]
