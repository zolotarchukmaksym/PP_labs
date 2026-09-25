from django.urls import path
from . import views
from . import plotly_dashboards, bokeh_dashboards

urlpatterns = [
    path('api/technician-repair-count/', views.technician_repair_count_view, name='technician_repair_count'),
    path('api/average-repair-cost-by-device/', views.average_repair_cost_by_device_view, name='average_repair_cost_by_device'),
    path('api/repair-status-count/', views.repair_status_count_view, name='repair_status_count'),
    path('api/customer-feedback-avg-rating/', views.customer_feedback_avg_rating_view, name='customer_feedback_avg_rating'),
    path('api/total-parts-cost-per-repair/', views.total_parts_cost_per_repair_view, name='total_parts_cost_per_repair'),
    path('api/average-repair-duration/', views.average_repair_duration_view, name='average_repair_duration'),
    path('api/basic-statistics/', views.basic_statistics, name='basic_statistics'),
    path('dashboard/plotly/', plotly_dashboards.plotly_dashboard, name='plotly_dashboard'),
    path('dashboard/bokeh/', bokeh_dashboards.bokeh_dashboard, name='bokeh_dashboard'),
]
