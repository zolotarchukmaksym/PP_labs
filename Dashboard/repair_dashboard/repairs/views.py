from django.db.models import Count, Avg, Sum, F, ExpressionWrapper, fields, Min, Max
from django.shortcuts import render
from django.http import JsonResponse
from .models import Technician, Device, Repair, Customer
import pandas as pd

# Агреговані запити

# Приклад 1: Кількість ремонтів для кожного техніка
technician_repair_count = Technician.objects.annotate(repair_count=Count('repair')).order_by('-repair_count')

# Приклад 2: Середня вартість ремонтів за типом пристроїв
average_repair_cost_by_device = Device.objects.values('device_type').annotate(avg_price=Avg('repairs__parts__price')).order_by('-avg_price')

# Приклад 3: Кількість ремонтів за статусом
repair_status_count = Repair.objects.values('status').annotate(count=Count('id')).order_by('-count')

# Приклад 4: Середній рейтинг зворотного зв'язку для кожного клієнта
customer_feedback_avg_rating = Customer.objects.annotate(avg_rating=Avg('feedback__rating')).order_by('-avg_rating')

# Приклад 5: Загальна вартість деталей для кожного ремонту
total_parts_cost_per_repair = Repair.objects.annotate(total_cost=Sum('parts__price')).order_by('-total_cost')

# Приклад 6: Середня тривалість ремонту (у днях)
average_repair_duration = Repair.objects.annotate(duration=ExpressionWrapper(F('completion_date') - F('repair_date'), output_field=fields.DurationField())).aggregate(average_duration=Avg('duration'))

# Ендпоїнти для отримання даних і перетворення їх у pandas DataFrame

def technician_repair_count_view(request):
    data = Technician.objects.annotate(repair_count=Count('repair')).order_by('-repair_count')
    df = pd.DataFrame(list(data.values()))
    return JsonResponse(df.to_dict(orient='records'), safe=False)

def average_repair_cost_by_device_view(request):
    data = Device.objects.values('device_type').annotate(avg_price=Avg('repairs__parts__price')).order_by('-avg_price')
    df = pd.DataFrame(list(data))
    return JsonResponse(df.to_dict(orient='records'), safe=False)

def repair_status_count_view(request):
    data = Repair.objects.values('status').annotate(count=Count('id')).order_by('-count')
    df = pd.DataFrame(list(data))
    return JsonResponse(df.to_dict(orient='records'), safe=False)

def customer_feedback_avg_rating_view(request):
    data = Customer.objects.annotate(avg_rating=Avg('feedback__rating')).order_by('-avg_rating')
    df = pd.DataFrame(list(data.values()))
    return JsonResponse(df.to_dict(orient='records'), safe=False)

def total_parts_cost_per_repair_view(request):
    data = Repair.objects.annotate(total_cost=Sum('parts__price')).order_by('-total_cost')
    df = pd.DataFrame(list(data.values()))
    return JsonResponse(df.to_dict(orient='records'), safe=False)

def average_repair_duration_view(request):
    data = Repair.objects.annotate(duration=ExpressionWrapper(F('completion_date') - F('repair_date'), output_field=fields.DurationField())).aggregate(average_duration=Avg('duration'))
    df = pd.DataFrame([data])
    return JsonResponse(df.to_dict(orient='records'), safe=False)

def basic_statistics(request):
    # Обчислення основних статистичних показників для кількох атрибутів
    repair_durations = Repair.objects.annotate(duration=ExpressionWrapper(F('completion_date') - F('repair_date'), output_field=fields.DurationField()))
    avg_duration = repair_durations.aggregate(Avg('duration'))['duration__avg']
    min_duration = repair_durations.aggregate(Min('duration'))['duration__min']
    max_duration = repair_durations.aggregate(Max('duration'))['duration__max']

    # Для обчислення медіани потрібно використовувати кастомний агрегат у Django
    median_duration = sorted([repair.duration for repair in repair_durations])[len(repair_durations) // 2]

    response_data = {
        'avg_duration': avg_duration,
        'min_duration': min_duration,
        'max_duration': max_duration,
        'median_duration': median_duration,
    }

    df = pd.DataFrame([response_data])
    return JsonResponse(df.to_dict(orient='records'), safe=False)
