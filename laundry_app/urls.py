from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('track/', views.track_order, name='track_order'),
    path('staff/login/', views.admin_login, name='admin_login'),
    path('staff/logout/', views.admin_logout, name='admin_logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('update-status/<int:order_id>/', views.update_status, name='update_status'),
    path('delete-order/<int:order_id>/', views.delete_order, name='delete_order'),
]
