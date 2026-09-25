from django.urls import path
from . import views

urlpatterns = [
    path('', views.technician_list, name='technician_list'),
    path('<int:id>/', views.technician_detail, name='technician_detail'),
    path('add/', views.technician_add, name='technician_add'),
    path('<int:id>/edit/', views.technician_edit, name='technician_edit'),
    path('<int:id>/delete/', views.technician_delete, name='technician_delete'),
]