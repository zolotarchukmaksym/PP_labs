from django.urls import path
from . import views
from .views import (
    RepairCountPerCustomer,
    AvgRepairTimePerTechnician,
    TotalCostPerRepairStatus,
    DeviceCountPerCategory,
    AvgRatingPerTechnician,
    TotalCostPerCustomerWithFilter,
)
from .views import (
    BasicStatistics,
    MedianRepairTime,
    GroupedByCategory,
    GroupedByMonth
)

urlpatterns = [
    path('repair-count-per-customer/', RepairCountPerCustomer.as_view(), name='repair_count_per_customer'),
    path('avg-repair-time-per-technician/', AvgRepairTimePerTechnician.as_view(), name='avg_repair_time_per_technician'),
    path('total-cost-per-repair-status/', TotalCostPerRepairStatus.as_view(), name='total_cost_per_repair_status'),
    path('device-count-per-category/', DeviceCountPerCategory.as_view(), name='device_count_per_category'),
    path('avg-rating-per-technician/', AvgRatingPerTechnician.as_view(), name='avg_rating_per_technician'),
    path('total-cost-per-customer-with-filter/', TotalCostPerCustomerWithFilter.as_view(), name='total_cost_per_customer_with_filter'),
    path('basic-statistics/', BasicStatistics.as_view(), name='basic_statistics'),
    path('median-repair-time/', MedianRepairTime.as_view(), name='median_repair_time'),
    path('grouped-by-category/', GroupedByCategory.as_view(), name='grouped_by_category'),
    path('grouped-by-month/', GroupedByMonth.as_view(), name='grouped_by_month'),
    path('dashboard_v1/', views.dashboard_v1, name='dashboard_v1'),
    path('dashboard_v2/', views.dashboard_v2, name='dashboard_v2'),
    path('performance_dashboard/', views.performance_dashboard, name='performance_dashboard'),
]

