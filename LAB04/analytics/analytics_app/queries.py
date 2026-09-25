from .models import Repair, Device, Feedback
from django.db.models import Count, Avg, Sum

repair_count_per_customer = Repair.objects.values('device__customer__name') \
    .annotate(repair_count=Count('id')) \
    .order_by('device__customer__name')

avg_repair_time_per_technician = Repair.objects.values('technician__name') \
    .annotate(avg_repair_time=Avg('repair_time')) \
    .order_by('technician__name')

total_cost_per_repair_status = Repair.objects.values('status__status_name') \
    .annotate(total_cost=Sum('cost')) \
    .order_by('status__status_name')

device_count_per_category = Device.objects.values('category') \
    .annotate(device_count=Count('id')) \
    .order_by('category')

avg_repair_cost_per_customer = Repair.objects.values('device__customer__name') \
    .annotate(avg_repair_cost=Avg('cost')) \
    .order_by('device__customer__name')

total_cost_per_customer_with_filter = Repair.objects.values('device__customer__name') \
    .annotate(total_cost=Sum('cost'), repair_count=Count('id')) \
    .filter(repair_count__gte=1) \
    .order_by('-total_cost')