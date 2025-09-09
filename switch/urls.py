from django.urls import path
from . import views

urlpatterns = [
    path('', views.switch_list_view, name='switch_list'),
    path('switch/add/', views.switch_add_view, name='switch_add'),
    path('switch/<int:pk>/', views.switch_detail_view, name='switch_detail'),
    path('update-status/', views.update_switch_status, name='update_switch_status'),
    path('switch/<int:pk>/cli/', views.switch_cli_view, name='switch_cli')
]